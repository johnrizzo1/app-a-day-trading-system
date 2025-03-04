import React, { useState, useEffect } from 'react';
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
  TableRow,
  Snackbar,
  Alert,
  AlertColor,
  SelectChangeEvent
} from '@mui/material';
import axios from 'axios';

interface Contract {
  id: number;
  symbol: string;
  expiry: string;
  tick_size: number;
  contract_size: number;
  margin_requirement: number;
}

interface Order {
  id: number;
  contract_id: number;
  type: string; // API returns 'type' not 'order_type'
  side: string;
  quantity: number;
  price?: number;
  status: string;
  created_at: string;
  updated_at: string;
  account_id: number;
  instrument_id: number;
  filled_quantity?: number;
}

interface SnackbarState {
  open: boolean;
  message: string;
  severity: AlertColor;
}

const Trading: React.FC = () => {
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [orders, setOrders] = useState<Order[]>([]);
  const [orderType, setOrderType] = useState('market');
  const [amount, setAmount] = useState('');
  const [price, setPrice] = useState('');
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<SnackbarState>({
    open: false,
    message: '',
    severity: 'success'
  });

  // Fetch available contracts when component mounts
  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const response = await axios.get('/api/trading/contracts');
        setContracts(response.data);
        if (response.data.length > 0) {
          setSelectedSymbol(response.data[0].id.toString());
        }
      } catch (error) {
        console.error('Error fetching contracts:', error);
        setSnackbar({
          open: true,
          message: 'Failed to fetch contracts',
          severity: 'error' as AlertColor
        });
      }
    };

    const fetchOrders = async () => {
      try {
        const response = await axios.get('/api/trading/orders');
        setOrders(response.data);
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    };

    fetchContracts();
    fetchOrders();
  }, []);

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleCancelOrder = async (orderId: number) => {
    setLoading(true);
    try {
      await axios.post(`/api/trading/orders/${orderId}/cancel`);
      
      // Refresh orders list
      const ordersResponse = await axios.get('/api/trading/orders');
      setOrders(ordersResponse.data);
      
      setSnackbar({
        open: true,
        message: 'Order cancelled successfully',
        severity: 'success' as AlertColor
      });
    } catch (error) {
      console.error('Error cancelling order:', error);
      setSnackbar({
        open: true,
        message: `Failed to cancel order: ${error.response?.data?.detail || error.message}`,
        severity: 'error' as AlertColor
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAmount(e.target.value);
  };

  const handlePriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPrice(e.target.value);
  };

  const handleBuy = async () => {
    if (!selectedSymbol || !amount) {
      setSnackbar({
        open: true,
        message: 'Please select a symbol and enter an amount',
        severity: 'error' as AlertColor
      });
      return;
    }

    setLoading(true);
    try {
      const orderData = {
        contract_id: parseInt(selectedSymbol),
        type: orderType.toLowerCase(),
        side: 'buy',
        quantity: parseFloat(amount),
        price: orderType !== 'market' ? parseFloat(price) : undefined
      };

      const response = await axios.post('/api/trading/orders', orderData);
      
      // Refresh orders list
      const ordersResponse = await axios.get('/api/trading/orders');
      setOrders(ordersResponse.data);
      
      setSnackbar({
        open: true,
        message: 'Buy order placed successfully',
        severity: 'success' as AlertColor
      });
      
      // Reset form
      setAmount('');
      if (orderType !== 'market') {
        setPrice('');
      }
    } catch (error) {
      console.error('Error placing buy order:', error);
      setSnackbar({
        open: true,
        message: `Failed to place order: ${error.response?.data?.detail || error.message}`,
        severity: 'error' as AlertColor
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSell = async () => {
    if (!selectedSymbol || !amount) {
      setSnackbar({
        open: true,
        message: 'Please select a symbol and enter an amount',
        severity: 'error' as AlertColor
      });
      return;
    }

    setLoading(true);
    try {
      const orderData = {
        contract_id: parseInt(selectedSymbol),
        type: orderType.toLowerCase(),
        side: 'sell',
        quantity: parseFloat(amount),
        price: orderType !== 'market' ? parseFloat(price) : undefined
      };

      const response = await axios.post('/api/trading/orders', orderData);
      
      // Refresh orders list
      const ordersResponse = await axios.get('/api/trading/orders');
      setOrders(ordersResponse.data);
      
      setSnackbar({
        open: true,
        message: 'Sell order placed successfully',
        severity: 'success' as AlertColor
      });
      
      // Reset form
      setAmount('');
      if (orderType !== 'market') {
        setPrice('');
      }
    } catch (error) {
      console.error('Error placing sell order:', error);
      setSnackbar({
        open: true,
        message: `Failed to place order: ${error.response?.data?.detail || error.message}`,
        severity: 'error' as AlertColor
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={3}>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
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
                  onChange={(e: SelectChangeEvent) => setSelectedSymbol(e.target.value)}
                >
                  {contracts.length > 0 ? (
                    contracts.map((contract) => (
                      <MenuItem key={contract.id} value={contract.id.toString()}>
                        {contract.symbol}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem value="" disabled>
                      No contracts available
                    </MenuItem>
                  )}
                </Select>
              </FormControl>

              <FormControl fullWidth margin="normal">
                <InputLabel>Order Type</InputLabel>
                <Select
                  value={orderType}
                  onChange={(e: SelectChangeEvent) => setOrderType(e.target.value)}
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
                value={amount}
                onChange={handleAmountChange}
                inputProps={{ min: 0, step: 0.01 }}
              />

              {orderType !== 'market' && (
                <TextField
                  fullWidth
                  label="Price"
                  type="number"
                  margin="normal"
                  value={price}
                  onChange={handlePriceChange}
                  inputProps={{ min: 0, step: 0.01 }}
                />
              )}

              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={6}>
                  <Button
                    variant="contained"
                    color="success"
                    fullWidth
                    onClick={handleBuy}
                    disabled={loading || !selectedSymbol || !amount}
                  >
                    Buy
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="contained"
                    color="error"
                    fullWidth
                    onClick={handleSell}
                    disabled={loading || !selectedSymbol || !amount}
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
                      <TableCell>{new Date(order.created_at).toLocaleString()}</TableCell>
                      <TableCell>
                        {contracts.find(c => c.id === order.contract_id)?.symbol || order.contract_id}
                      </TableCell>
                      <TableCell>{order.type}</TableCell>
                      <TableCell align="right">{order.side}</TableCell>
                      <TableCell align="right">{order.quantity}</TableCell>
                      <TableCell align="right">{order.price || 'Market'}</TableCell>
                      <TableCell align="right">{order.status}</TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          color="error"
                          onClick={() => handleCancelOrder(order.id)}
                          disabled={order.status !== 'pending' && order.status !== 'open'}
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
