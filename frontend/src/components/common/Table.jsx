/**
 * Reusable Table component.
 * Following the common-modules.md specification.
 */
import React from 'react';
import {
  Table as MuiTable,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableContainer,
  Paper,
} from '@mui/material';

/**
 * Custom Table component wrapping MUI Table.
 * Provides consistent table styling and structure.
 *
 * @param {Object} props - Component props
 * @param {Array} props.columns - Column definitions [{id: string, label: string}]
 * @param {Array} props.data - Data rows (array of objects)
 * @param {boolean} props.stickyHeader - Whether header should stick on scroll
 * @returns {JSX.Element} Table component
 */
export const Table = ({ columns, data, stickyHeader = false }) => {
  return (
    <TableContainer component={Paper}>
      <MuiTable stickyHeader={stickyHeader}>
        <TableHead>
          <TableRow>
            {columns.map((col) => (
              <TableCell key={col.id} align={col.align || 'left'}>
                {col.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index} hover>
              {columns.map((col) => (
                <TableCell key={col.id} align={col.align || 'left'}>
                  {row[col.id]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </MuiTable>
    </TableContainer>
  );
};

export default Table;
