"use client";

import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Zap, RefreshCw } from "lucide-react";
import toast from "react-hot-toast";
import FileUpload from "@/components/FileUpload";
import ValidationResult from "@/components/ValidationResult";
import { ValidationResult as ValidationResultType } from "@/types";
import { api, APIError } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState<
    "idle" | "processing" | "completed" | "error"
  >("idle");
  const [result, setResult] = useState<ValidationResultType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const processStartupIdea = useCallback(
    async (content: string, fileType: "text" | "pdf" | "docx" = "text") => {
      setStatus("processing");
      setResult(null);
      setError(null);

      try {
        // Make API call to backend
        const response = await api.validateStartupIdea(content, fileType);
        setResult(response);
        setStatus("completed");
        toast.success("Startup validation completed!");
      } catch (error) {
        console.error("Validation error:", error);

        if (error instanceof APIError) {
          setError(error.message);
          toast.error(`API Error: ${error.message}`);
        } else {
          setError("An unexpected error occurred. Please try again.");
          toast.error("An unexpected error occurred. Please try again.");
        }

        setStatus("error");
      }
    },
    []
  );

  const handleFileSelect = useCallback(async (file: File, content: string) => {
    setStatus("processing");
    setResult(null);
    setError(null);

    try {
      // Make API call to backend for file validation
      const response = await api.validateFile(file);
      setResult(response);
      setStatus("completed");
      toast.success("Startup validation completed!");
    } catch (error) {
      console.error("File validation error:", error);

      if (error instanceof APIError) {
        setError(error.message);
        toast.error(`API Error: ${error.message}`);
      } else {
        setError("An unexpected error occurred. Please try again.");
        toast.error("An unexpected error occurred. Please try again.");
      }

      setStatus("error");
    }
  }, []);

  const handleTextInput = useCallback(
    (text: string) => {
      processStartupIdea(text, "text");
    },
    [processStartupIdea]
  );

  const handleReset = useCallback(() => {
    setStatus("idle");
    setResult(null);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 to-secondary-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <Zap className="w-12 h-12 text-primary-600 mr-3" />
            <h1 className="text-4xl font-bold text-gradient">
              Startup Guillotine
            </h1>
          </div>
          <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
            Validate your startup idea with AI-powered comprehensive analysis
            and real-time market research
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {status === "idle" && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <FileUpload
                onFileSelect={handleFileSelect}
                onTextInput={handleTextInput}
              />
            </motion.div>
          )}

          {status === "processing" && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <div className="card text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
                <h2 className="text-2xl font-semibold mb-4">
                  Analyzing Your Startup Idea
                </h2>
                <p className="text-secondary-600 mb-6">
                  We're performing comprehensive analysis using multiple data
                  sources...
                </p>
                <div className="space-y-2 text-sm text-secondary-500">
                  <p>• Analyzing Google Trends data</p>
                  <p>• Researching competitive landscape</p>
                  <p>• Gathering community insights</p>
                  <p>• Generating comprehensive business analysis</p>
                </div>
              </div>
            </motion.div>
          )}

          {status === "completed" && result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-semibold">
                  Comprehensive Analysis Results
                </h2>
                <button
                  onClick={handleReset}
                  className="btn-secondary flex items-center"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Analyze Another Idea
                </button>
              </div>
              <ValidationResult result={result} />
            </motion.div>
          )}

          {status === "error" && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card text-center"
            >
              <h2 className="text-2xl font-semibold mb-4 text-red-600">
                Analysis Failed
              </h2>
              <p className="text-secondary-600 mb-6">
                {error || "Something went wrong while analyzing your startup idea. Please try again."}
              </p>
              <button onClick={handleReset} className="btn-primary">
                Try Again
              </button>
            </motion.div>
          )}
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-16 text-secondary-500"
        >
          <p>Powered by Gemini 1.5 Flash & Comprehensive Market Analysis</p>
        </motion.div>
      </div>
    </div>
  );
}
