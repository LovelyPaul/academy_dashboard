/**
 * Bar Chart component using Chart.js.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

/**
 * Bar Chart component for displaying categorical data.
 *
 * @param {Object} props - Component props
 * @param {Object} props.data - Chart data in Chart.js format
 * @param {Object} props.options - Chart options in Chart.js format
 * @returns {JSX.Element} Bar Chart component
 */
export const BarChart = ({ data, options }) => {
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

  return <Bar data={data} options={defaultOptions} />;
};

export default BarChart;
