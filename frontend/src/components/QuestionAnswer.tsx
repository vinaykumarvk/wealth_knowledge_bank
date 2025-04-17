import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';

interface Source {
  page: string;
  file: string;
  content: string;
}

interface Answer {
  answer: string;
  sources: Source[];
}

const QuestionAnswer: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<Answer | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post<Answer>('http://localhost:8000/ask', {
        text: question,
      });
      setAnswer(response.data);
    } catch (error) {
      console.error('Error asking question:', error);
      setError('Error getting answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <TextField
        fullWidth
        label="Enter your question"
        variant="outlined"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        multiline
        rows={3}
      />
      
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={loading || !question.trim()}
        sx={{ alignSelf: 'flex-end' }}
      >
        {loading ? <CircularProgress size={24} /> : 'Ask Question'}
      </Button>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      {answer && (
        <Paper elevation={3} sx={{ p: 3, mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Answer:
          </Typography>
          <Typography paragraph>
            {answer.answer}
          </Typography>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Sources:
          </Typography>
          {answer.sources.map((source, index) => (
            <Accordion key={index}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>
                  {source.file} (Page {source.page})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                  {source.content}
                </Typography>
              </AccordionDetails>
            </Accordion>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default QuestionAnswer; 