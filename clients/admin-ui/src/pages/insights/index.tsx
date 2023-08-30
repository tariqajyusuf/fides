import type { NextPage } from "next";

import HomeLayout from "~/home/HomeLayout";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Doughnut, Bar, Line } from "react-chartjs-2";
import { Box, SimpleGrid } from "@fidesui/react";

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const donutData = {
  labels: [
    'Unreviewed',
    'In Progress',
    'Complete'
  ],
  datasets: [{
    data: [300, 50, 100],
    backgroundColor: [
      '#63B3ED',
      '#B794F4',
      '#4FD1C5'
    ],
    hoverOffset: 4
  }]
};
const donutOptions = {
  plugins: {
    title: {
      display: true,
      text: 'Requests per Status',
    },
  }
};

const barOptions = {
  plugins: {
    title: {
      display: true,
      text: 'Requests per Policy',
    },
  },
  responsive: true,
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true,
    },
  },
};
const barLabels = ['January', 'February', 'March', 'April', 'May'];

const barData = {
  labels: barLabels,
  // maintainAspectRatio: false,
  datasets: [
    {
      label: 'Access',
      data: [53, 78, 134, 97, 83],
      backgroundColor: '#4FD1C5',
    },
    {
      label: 'Erasure',
      data: [22, 99, 103, 44, 94],
      backgroundColor: '#F687B3',
    },
    {
      label: 'Consent',
      data: [242, 299, 143, 144, 294],
      backgroundColor: '#F6AD55',
    },
  ],
};

const Insights: NextPage = () => {

  return (
    <HomeLayout title="Insights">
      <SimpleGrid columns={{ md: 2, xl: 3 }} spacing="24px">
        <Box pl='30px' height="375px">
          <Doughnut options={donutOptions} data={donutData} />
        </Box>
        <Box>
          <Bar height="250px" options={barOptions} data={barData} />
        </Box>
      </SimpleGrid>
    </HomeLayout>
  );
};
export default Insights;
