import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const PortfolioMonitor: React.FC = () => {
  const [positions, setPositions] = React.useState([]);
  const [performance, setPerformance] = React.useState([]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Portfolio Monitor
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6">Portfolio Performance</Typography>
              <LineChart width={600} height={300} data={performance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
              </LineChart>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Asset Allocation</Typography>
              <PieChart width={300} height={300}>
                <Pie
                  data={positions}
                  cx={150}
                  cy={150}
                  labelLine={false}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {positions.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Current Positions</Typography>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Asset</TableCell>
                    <TableCell align="right">Position</TableCell>
                    <TableCell align="right">Entry Price</TableCell>
                    <TableCell align="right">Current Price</TableCell>
                    <TableCell align="right">P&L</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {positions.map((position) => (
                    <TableRow key={position.asset}>
                      <TableCell>{position.asset}</TableCell>
                      <TableCell align="right">{position.size}</TableCell>
                      <TableCell align="right">{position.entryPrice}</TableCell>
                      <TableCell align="right">{position.currentPrice}</TableCell>
                      <TableCell align="right">{position.pnl}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PortfolioMonitor;
