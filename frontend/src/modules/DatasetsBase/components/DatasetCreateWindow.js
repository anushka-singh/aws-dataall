import { CloudDownloadOutlined } from '@mui/icons-material';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Dialog,
  Grid,
  Typography
} from '@mui/material';
import PropTypes from 'prop-types';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { PlusIcon } from '../../../design';
import { isModuleEnabled, ModuleNames } from 'utils';

export const DatasetCreateWindow = (props) => {
  const { onClose, open, ...other } = props;
  const number_grid_items = isModuleEnabled(ModuleNames.S3_DATASETS) ? 2 : 0;
  const width_grid_item = number_grid_items > 0 ? 12 / number_grid_items : 1;

  return (
    <Dialog maxWidth="md" fullWidth onClose={onClose} open={open} {...other}>
      <Box sx={{ m: 4 }}>
        <Grid
          container
          spacing={2}
          alignItems="flex-start"
          justifyContent="center"
        >
          {isModuleEnabled(ModuleNames.S3_DATASETS) && (
            <Grid
              item
              justifyContent="center"
              md={width_grid_item}
              lg={width_grid_item}
              xl={width_grid_item}
            >
              <Card>
                <CardHeader title="Create S3-Glue Dataset" />
                <CardContent>
                  <Typography
                    color="textSecondary"
                    gutterBottom
                    variant="subtitle2"
                  >
                    Data.all will create an S3 Bucket encrypted with KMS key and
                    a Glue database.
                  </Typography>
                  <Button
                    color="primary"
                    component={RouterLink}
                    startIcon={<PlusIcon fontSize="small" />}
                    sx={{ m: 1 }}
                    to="/console/s3-datasets/new"
                    variant="contained"
                  >
                    Create
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          )}
          {isModuleEnabled(ModuleNames.S3_DATASETS) && (
            <Grid
              item
              justifyContent="center"
              md={width_grid_item}
              lg={width_grid_item}
              xl={width_grid_item}
            >
              <Card>
                <CardHeader title="Import S3-Glue Dataset" />
                <CardContent>
                  <Typography
                    color="textSecondary"
                    gutterBottom
                    variant="subtitle2"
                  >
                    Data.all will use the S3 Bucket as it is encrypted and will
                    create a Glue database if you do not provide one.
                  </Typography>
                  <Button
                    color="primary"
                    component={RouterLink}
                    startIcon={<CloudDownloadOutlined fontSize="small" />}
                    sx={{ m: 1 }}
                    to="/console/s3-datasets/import"
                    variant="outlined"
                  >
                    Import
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Box>
    </Dialog>
  );
};

DatasetCreateWindow.propTypes = {
  onClose: PropTypes.func,
  open: PropTypes.bool.isRequired
};
