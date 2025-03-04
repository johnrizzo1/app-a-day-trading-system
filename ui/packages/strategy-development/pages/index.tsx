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
  InputLabel
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const StrategyDevelopment: React.FC = () => {
  const [strategies, setStrategies] = React.useState([]);
  const [selectedModel, setSelectedModel] = React.useState('');

  return (
    <Box p={3}>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Strategy Configuration</Typography>
              <TextField
                fullWidth
                label="Strategy Name"
                margin="normal"
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Select Model</InputLabel>
                <Select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  <MenuItem value="">None</MenuItem>
                  {/* Models will be populated here */}
                </Select>
              </FormControl>
              <TextField
                fullWidth
                label="Parameters"
                margin="normal"
                multiline
                rows={4}
              />
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
              >
                Save Strategy
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6">Strategy Performance</Typography>
              <LineChart width={600} height={300} data={[]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
              </LineChart>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StrategyDevelopment;
