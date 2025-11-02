import React from 'react';
import { Box, Grid, Card, CardContent, Skeleton } from '@mui/material';

/**
 * Skeleton Loader Component
 *
 * Displays loading placeholders while data is being fetched
 */
export default function SkeletonLoader() {
  return (
    <Box>
      {/* Header Skeleton */}
      <Box mb={3}>
        <Skeleton variant="text" width="30%" height={40} />
        <Skeleton variant="text" width="50%" height={20} />
      </Box>

      {/* Filter Panel Skeleton */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            {[1, 2, 3, 4].map((i) => (
              <Grid item xs={12} sm={6} md={3} key={i}>
                <Skeleton variant="rectangular" height={56} />
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Charts Skeleton */}
      <Grid container spacing={3}>
        {/* Trend Chart Skeleton */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Skeleton variant="text" width="40%" height={30} sx={{ mb: 2 }} />
              <Skeleton variant="rectangular" height={300} />
            </CardContent>
          </Card>
        </Grid>

        {/* Department Chart Skeleton */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Skeleton variant="text" width="40%" height={30} sx={{ mb: 2 }} />
              <Skeleton variant="rectangular" height={300} />
            </CardContent>
          </Card>
        </Grid>

        {/* Achievement Card Skeleton */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Skeleton variant="text" width="60%" height={30} sx={{ mb: 2 }} />
              <Skeleton variant="circular" width={100} height={100} sx={{ mx: 'auto', mb: 2 }} />
              <Skeleton variant="rectangular" height={10} sx={{ mb: 2 }} />
              <Skeleton variant="text" />
              <Skeleton variant="text" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
