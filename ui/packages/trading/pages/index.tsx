import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from '@mui/material';

const Trading: React.FC = () => {
  const [selectedSymbol, setSelectedSymbol] = React.useState('');
  const [orders, setOrders] = React.useState([]);
  const [orderType, setOrderType] = React.useState('market');

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Trading Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">New Order</Typography>
              <FormControl fullWidth margin="normal">
                <InputLabel>Symbol</InputLabel>
                <Select
                  value={selectedSymbol}
                  onChange={(e) => setSelectedSymbol(e.target.value)}
                >
                  <MenuItem value="BTC/USD">BTC/USD</MenuItem>
                  <MenuItem value="ETH/USD">ETH/USD</MenuItem>
                  <MenuItem value="SOL/USD">SOL/USD</MenuItem>
                </Select>
              </FormControl>

              <FormControl fullWidth margin="normal">
                <InputLabel>Order Type</InputLabel>
                <Select
                  value={orderType}
                  onChange={(e) => setOrderType(e.target.value)}
                >
                  <MenuItem value="market">Market</MenuItem>
                  <MenuItem value="limit">Limit</MenuItem>
                  <MenuItem value="stop">Stop</MenuItem>
                </Select>
              </FormControl>

              <TextField
                fullWidth
                label="Amount"
                type="number"
                margin="normal"
              />

              {orderType !== 'market' && (
                <TextField
                  fullWidth
                  label="Price"
                  type="number"
                  margin="normal"
                />
              )}

              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={6}>
                  <Button
                    variant="contained"
                    color="success"
                    fullWidth
                  >
                    Buy
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="contained"
                    color="error"
                    fullWidth
                  >
                    Sell
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6">Market Data</Typography>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Symbol</TableCell>
                    <TableCell align="right">Last Price</TableCell>
                    <TableCell align="right">24h Change</TableCell>
                    <TableCell align="right">24h Volume</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {/* Market data will be populated here */}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6">Active Orders</Typography>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Time</TableCell>
                    <TableCell>Symbol</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell align="right">Side</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell align="right">Price</TableCell>
                    <TableCell align="right">Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {orders.map((order) => (
                    <TableRow key={order.id}>
                      <TableCell>{order.time}</TableCell>
                      <TableCell>{order.symbol}</TableCell>
                      <TableCell>{order.type}</TableCell>
                      <TableCell align="right">{order.side}</TableCell>
                      <TableCell align="right">{order.amount}</TableCell>
                      <TableCell align="right">{order.price}</TableCell>
                      <TableCell align="right">{order.status}</TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          color="error"
                          onClick={() => {/* Cancel order */}}
                        >
                          Cancel
                        </Button>
                      </TableCell>
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

export default Trading;
