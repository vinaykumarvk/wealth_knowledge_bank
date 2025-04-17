import React, { useState } from 'react';
import { 
  Container, 
  CssBaseline, 
  ThemeProvider, 
  createTheme,
  Box,
  Typography,
  AppBar,
  Toolbar,
  Paper
} from '@mui/material';
import FileUpload from './components/FileUpload';
import QuestionAnswer from './components/QuestionAnswer';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Wealth Knowledge Bank
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Upload Documents
            </Typography>
            <FileUpload onUploadSuccess={setUploadSuccess} />
            {uploadSuccess && (
              <Typography color="success.main" sx={{ mt: 2 }}>
                {uploadSuccess}
              </Typography>
            )}
          </Paper>
          
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Ask Questions
            </Typography>
            <QuestionAnswer />
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
