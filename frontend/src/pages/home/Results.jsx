import React from 'react'
import { TableContainer, Table, TableHead, TableRow, TableCell, Paper, TableBody } from '@mui/material'

function Results({ data }) {
  return (
    <TableContainer component={Paper}>
        <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    {data[0].map((header) => (
                        <TableCell>{header}</TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
            {data.slice(1).map((row) => (
                <TableRow>
                    {row.map((cell) => (
                        <TableCell>{cell}</TableCell>
                    ))}
                </TableRow>
            ))}
            </TableBody>
        </Table>
    </TableContainer>
  )
}

export default Results