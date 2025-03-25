import React, { useState } from "react";
import {
  Container,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
} from "@mui/material";
import axios from "axios";
import { config } from "../config/config";

export const EmailCategorizer: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [response, setResponse] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setResponse("");
      setError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResponse("");
    setLoading(true);

    if (!file) {
      setError("Please upload an .eml file.");
      setLoading(false);
      return;
    }

    try {
      const fileContent = await file.text(); // Read the file content as text

      const res = await axios.post(`${config.API_BASE_URL}/generate`, {
        message: fileContent,
      });

      setResponse(res.data.response);
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError("Failed to connect to the server.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: "50px" }}>
      <Typography variant="h4" gutterBottom>
        Generate Response from EML File
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <Button
          variant="contained"
          component="label"
          color="primary"
        >
          Upload EML File
          <input
            type="file"
            accept=".eml"
            hidden
            onChange={handleFileChange}
          />
        </Button>
        {file && (
          <Typography variant="body1">
            Selected File: {file.name}
          </Typography>
        )}
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Submit"}
        </Button>
      </Box>
      {response && (
        <Alert severity="success" style={{ marginTop: "20px" }}>
          <strong>Response:</strong> {response}
        </Alert>
      )}
      {error && (
        <Alert severity="error" style={{ marginTop: "20px" }}>
          <strong>Error:</strong> {error}
        </Alert>
      )}
    </Container>
  );
};