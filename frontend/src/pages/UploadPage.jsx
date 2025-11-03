/**
 * Upload Page Component
 * Admin page for uploading data files (Excel).
 * Displays upload form and upload history.
 */

import React, { useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Alert,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { MainLayout } from '../layouts/MainLayout';
import { useApiClient } from '../hooks/useApiClient';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const { getAuthenticatedClient } = useApiClient();

  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Validate file type
      const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
      if (!['xlsx', 'xls', 'csv'].includes(fileExtension)) {
        setError('Excel 또는 CSV 파일만 업로드 가능합니다 (.xlsx, .xls, .csv)');
        return;
      }
      setFile(selectedFile);
      setError(null);
      setUploadResult(null);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError('파일을 선택해주세요.');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadResult(null);

    try {
      const client = await getAuthenticatedClient();
      const formData = new FormData();
      formData.append('file', file);

      const response = await client.post('/dashboard/upload/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResult(response.data);
      setFile(null);

      // Reset file input
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.value = '';

      // Refresh upload history
      fetchUploadHistory();
    } catch (err) {
      setError(
        err.response?.data?.error?.message ||
        '업로드 중 오류가 발생했습니다.'
      );
    } finally {
      setUploading(false);
    }
  };

  // Fetch upload history
  const fetchUploadHistory = useCallback(async () => {
    try {
      const client = await getAuthenticatedClient();
      const response = await client.get('/dashboard/upload/history/');
      setHistory(response.data.items || []);
    } catch (err) {
      console.error('Failed to fetch upload history:', err);
    }
  }, [getAuthenticatedClient]);

  // Fetch history on mount
  React.useEffect(() => {
    fetchUploadHistory();
  }, [fetchUploadHistory]);

  return (
    <MainLayout>
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Typography variant="h4" component="h1" gutterBottom>
          데이터 업로드
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 4 }}>
          Excel 또는 CSV 파일을 업로드하여 데이터를 가져올 수 있습니다.
        </Typography>

        {/* Upload Section */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            파일 업로드
          </Typography>

          {/* File Input */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <input
              id="file-input"
              type="file"
              accept=".xlsx,.xls,.csv"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input">
              <Button
                variant="outlined"
                component="span"
                startIcon={<CloudUploadIcon />}
                disabled={uploading}
              >
                파일 선택
              </Button>
            </label>
            {file && (
              <Typography variant="body2" color="textSecondary">
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </Typography>
            )}
          </Box>

          {/* Upload Button */}
          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={!file || uploading}
            sx={{ mb: 2 }}
          >
            {uploading ? '업로드 중...' : '업로드'}
          </Button>

          {/* Progress Bar */}
          {uploading && <LinearProgress sx={{ mb: 2 }} />}

          {/* Error Message */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Success Message */}
          {uploadResult && uploadResult.success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              업로드 성공! {uploadResult.records_processed || 0}개 행이 가져와졌습니다.
            </Alert>
          )}

          {/* Upload Result Details */}
          {uploadResult && !uploadResult.success && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              업로드 실패: {uploadResult.error || '알 수 없는 오류'}
            </Alert>
          )}
        </Paper>

        {/* Upload History */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            업로드 히스토리
          </Typography>

          {history.length === 0 ? (
            <Typography variant="body2" color="textSecondary">
              업로드 내역이 없습니다.
            </Typography>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>파일명</TableCell>
                    <TableCell>업로드 시간</TableCell>
                    <TableCell>상태</TableCell>
                    <TableCell align="right">가져온 행 수</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {history.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item.filename || 'N/A'}</TableCell>
                      <TableCell>
                        {item.uploaded_at
                          ? new Date(item.uploaded_at).toLocaleString('ko-KR')
                          : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={item.status === 'success' ? '성공' : '실패'}
                          color={item.status === 'success' ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        {item.rows_imported || 0}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      </Box>
    </MainLayout>
  );
};

export default UploadPage;
