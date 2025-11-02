import React, { useState } from 'react';
import {
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip
} from '@mui/material';
import { useBudget } from '../../contexts/BudgetContext';

export default function BudgetDataTable() {
  const { state } = useBudget();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const getStatusChip = (status) => {
    const config = {
      normal: { label: 'Normal', color: 'success' },
      warning: { label: 'Warning', color: 'warning' },
      critical: { label: 'Critical', color: 'error' }
    };
    const { label, color } = config[status] || config.normal;
    return <Chip label={label} color={color} size="small" />;
  };

  const paginatedData = state.executionStatus.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Card>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Department</TableCell>
              <TableCell align="right">Total Budget</TableCell>
              <TableCell align="right">Executed Amount</TableCell>
              <TableCell align="right">Execution Rate</TableCell>
              <TableCell align="right">Remaining</TableCell>
              <TableCell align="center">Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.department}</TableCell>
                <TableCell align="right">{row.total_budget?.toLocaleString()}</TableCell>
                <TableCell align="right">{row.executed_amount?.toLocaleString()}</TableCell>
                <TableCell align="right">{row.execution_rate}%</TableCell>
                <TableCell align="right">{row.remaining_budget?.toLocaleString()}</TableCell>
                <TableCell align="center">{getStatusChip(row.status)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={state.executionStatus.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={(_, newPage) => setPage(newPage)}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10));
          setPage(0);
        }}
      />
    </Card>
  );
}
