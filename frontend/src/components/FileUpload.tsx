"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText, File, X } from "lucide-react";
import { motion } from "framer-motion";
import {
  formatFileSize,
  validateFileType,
  validateFileSize,
} from "@/lib/utils";
import { api } from "@/lib/api";

interface FileUploadProps {
  onFileSelect: (file: File, content: string) => void;
  onTextInput: (text: string) => void;
  disabled?: boolean;
}

export default function FileUpload({
  onFileSelect,
  onTextInput,
  disabled,
}: FileUploadProps) {
  const [textInput, setTextInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null);
      const file = acceptedFiles[0];

      if (!file) return;

      // Validate file type
      const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ];
      if (!validateFileType(file, allowedTypes)) {
        setError("Please upload a PDF or DOCX file");
        return;
      }

      // Validate file size (10MB max)
      if (!validateFileSize(file, 10)) {
        setError("File size must be less than 10MB");
        return;
      }

      setSelectedFile(file);

      // Use the file validation API
      onFileSelect(file, "");
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
    },
    maxFiles: 1,
    disabled,
  });

  const handleTextSubmit = () => {
    if (textInput.trim()) {
      onTextInput(textInput.trim());
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    setError(null);
  };

  const getFileIcon = (file: File) => {
    if (file.type === "application/pdf") {
      return <File className="w-8 h-8 text-red-500" />;
    }
    return <FileText className="w-8 h-8 text-blue-500" />;
  };

  return (
    <div className="space-y-6">
      {/* Text Input */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">
          Or describe your startup idea
        </h3>
        <textarea
          className="input-field min-h-[120px] resize-none"
          placeholder="Describe your startup idea here... (problem, solution, target audience, etc.)"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          disabled={disabled}
        />
        <button
          onClick={handleTextSubmit}
          disabled={!textInput.trim() || disabled}
          className="btn-primary mt-3 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Analyze Startup Idea
        </button>
      </div>

      {/* File Upload */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Or upload a document</h3>

        {selectedFile ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg border border-secondary-200"
          >
            <div className="flex items-center space-x-3">
              {getFileIcon(selectedFile)}
              <div>
                <div className="font-medium">{selectedFile.name}</div>
                <div className="text-sm text-secondary-600">
                  {formatFileSize(selectedFile.size)}
                </div>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-1 hover:bg-secondary-200 rounded-full transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        ) : (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? "border-primary-400 bg-primary-50"
                : "border-secondary-300 hover:border-secondary-400"
            } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 mx-auto mb-4 text-secondary-400" />
            <p className="text-lg font-medium mb-2">
              {isDragActive ? "Drop your file here" : "Drag & drop a file here"}
            </p>
            <p className="text-secondary-600 mb-4">
              or click to select a PDF or DOCX file
            </p>
            <p className="text-sm text-secondary-500">
              Maximum file size: 10MB
            </p>
          </div>
        )}

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
          >
            {error}
          </motion.div>
        )}
      </div>
    </div>
  );
}
