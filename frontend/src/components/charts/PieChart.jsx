/**
 * Pie Chart component using Chart.js.
 * Following the common-modules.md specification.
 */
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

/**
 * Pie Chart component for displaying proportional data.
 *
 * @param {Object} props - Component props
 * @param {Object} props.data - Chart data in Chart.js format
 * @param {Object} props.options - Chart options in Chart.js format
 * @returns {JSX.Element} Pie Chart component
 */
export const PieChart = ({ data, options }) => {
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: false,
      },
    },
    ...options,
  };

  return <Pie data={data} options={defaultOptions} />;
};

export default PieChart;
