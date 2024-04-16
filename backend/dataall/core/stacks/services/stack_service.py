import os

import requests

from dataall.core.environment.db.environment_repositories import EnvironmentRepository
from dataall.core.tasks.service_handlers import Worker
from dataall.base.config import config
from dataall.base.context import get_context
from dataall.core.environment.db.environment_models import Environment
from dataall.core.stacks.aws.ecs import Ecs
from dataall.core.stacks.db.stack_repositories import StackRepository
from dataall.core.stacks.db.stack_models import Stack
from dataall.core.tasks.db.task_models import Task
from dataall.base.utils import Parameter


class StackService:
    @staticmethod
    def get_stack_with_cfn_resources(targetUri: str, environmentUri: str):
        context = get_context()
        with context.db_engine.scoped_session() as session:
            env: Environment = EnvironmentRepository.get_environment_by_uri(session, environmentUri)
            stack: Stack = StackRepository.find_stack_by_target_uri(session, target_uri=targetUri)
            if not stack:
                stack = Stack(
                    stack='environment',
                    payload={},
                    targetUri=targetUri,
                    accountid=env.AwsAccountId if env else 'UNKNOWN',
                    region=env.region if env else 'UNKNOWN',
                    resources=str({}),
                    error=str({}),
                    outputs=str({}),
                )
                return stack

            cfn_task = StackService.save_describe_stack_task(session, env, stack, targetUri)
            Worker.queue(engine=context.db_engine, task_ids=[cfn_task.taskUri])
        return stack

    @staticmethod
    def save_describe_stack_task(session, environment, stack, target_uri):
        cfn_task = Task(
            targetUri=stack.stackUri,
            action='cloudformation.stack.describe_resources',
            payload={
                'accountid': environment.AwsAccountId,
                'region': environment.region,
                'role_arn': environment.CDKRoleArn,
                'stack_name': stack.name,
                'stackUri': stack.stackUri,
                'targetUri': target_uri,
            },
        )
        session.add(cfn_task)
        session.commit()
        return cfn_task

    @staticmethod
    def deploy_stack(targetUri):
        context = get_context()
        with context.db_engine.scoped_session() as session:
            stack: Stack = StackRepository.get_stack_by_target_uri(session, target_uri=targetUri)
            envname = os.getenv('envname', 'local')

            if envname in ['local', 'pytest', 'dkrcompose']:
                requests.post(f'{config.get_property("cdk_proxy_url")}/stack/{stack.stackUri}')

            else:
                cluster_name = Parameter().get_parameter(env=envname, path='ecs/cluster/name')
                if not Ecs.is_task_running(cluster_name, f'awsworker-{stack.stackUri}'):
                    stack.EcsTaskArn = Ecs.run_cdkproxy_task(stack.stackUri)
                else:
                    task: Task = Task(action='ecs.cdkproxy.deploy', targetUri=stack.stackUri)
                    session.add(task)
                    session.commit()
                    Worker.queue(engine=context.db_engine, task_ids=[task.taskUri])

            return stack

    @staticmethod
    def delete_stack(target_uri, accountid, cdk_role_arn, region):
        context = get_context()
        with context.db_engine.scoped_session() as session:
            stack: Stack = StackRepository.find_stack_by_target_uri(session, target_uri=target_uri)
            if not stack:
                return
            task = Task(
                targetUri=target_uri,
                action='cloudformation.stack.delete',
                payload={
                    'accountid': accountid,
                    'region': region,
                    'cdk_role_arn': cdk_role_arn,
                    'stack_name': stack.name,
                },
            )
            session.add(task)

        Worker.queue(context.db_engine, [task.taskUri])
        return True