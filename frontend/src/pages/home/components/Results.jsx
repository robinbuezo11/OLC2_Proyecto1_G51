import React from 'react'
import { TableContainer, Table, TableHead, TableRow, TableCell, Paper, TableBody } from '@mui/material'

function Results({ data }) {
  return (
    <TableContainer component={Paper}>
        <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    {data[0].map((header,index) => (
                        <TableCell key={index}>
                            {header}
                        </TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
            {data.slice(1).map((row, index) => (
                <TableRow key={index}>
                    {row.map((cell,index1) => (
                        <TableCell key={index1}>
                            {cell}
                        </TableCell>
                    ))}
                </TableRow>
            ))}
            </TableBody>
        </Table>
    </TableContainer>
  )
}

export default Results