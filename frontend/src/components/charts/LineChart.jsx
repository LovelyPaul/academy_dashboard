/**
 * Line Chart component using Chart.js.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

/**
 * Line Chart component for displaying time-series or trend data.
 *
 * @param {Object} props - Component props
 * @param {Object} props.data - Chart data in Chart.js format
 * @param {Object} props.options - Chart options in Chart.js format
 * @returns {JSX.Element} Line Chart component
 */
export const LineChart = ({ data, options }) => {
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
      },
    },
    ...options,
  };

  return <Line data={data} options={defaultOptions} />;
};

export default LineChart;
