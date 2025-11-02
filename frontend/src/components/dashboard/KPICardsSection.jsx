/**
 * KPI Cards Section Component
 * Displays 4 KPI cards: 총 실적, 논문 수, 학생 수, 예산 현황
 * Follows the plan.md specifications.
 */

import { Grid, Skeleton } from '@mui/material';
import { useDashboard } from '../../context/DashboardContext';
import { KPICard } from '../charts/KPICard';
import { formatNumber, formatPercentage, formatCurrency } from '../../utils/formatters';

/**
 * KPI Cards Section Component
 * Renders 4 KPI metric cards in a responsive grid.
 */
export const KPICardsSection = () => {
  const { kpiData, isLoading, error } = useDashboard();

  // Show loading skeletons
  if (isLoading) {
    return (
      <Grid container spacing={3}>
        {[1, 2, 3, 4].map((i) => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <Skeleton variant="rectangular" height={150} />
          </Grid>
        ))}
      </Grid>
    );
  }

  // Don't render if there's an error or no data
  if (error || !kpiData) {
    return null;
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <KPICard
          title="총 실적"
          value={formatPercentage(kpiData.total_performance)}
          subtitle="평균 취업률"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <KPICard
          title="논문 게재 수"
          value={formatNumber(kpiData.publication_count)}
          subtitle="올해"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <KPICard
          title="학생 수"
          value={formatNumber(kpiData.student_count)}
          subtitle="재학생"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <KPICard
          title="예산 집행률"
          value={formatPercentage(kpiData.budget_status.rate)}
          subtitle={`${formatCurrency(kpiData.budget_status.executed)} / ${formatCurrency(kpiData.budget_status.total)}`}
        />
      </Grid>
    </Grid>
  );
};
