# SOMA Organized Output System

This folder contains all tokenization outputs organized by tokenizer type and file format.

## 📁 Folder Structure

```
Outputs/
├── space/          # Space-based tokenization
│   ├── JSON/       # JSON format files
│   ├── CSV/        # CSV format files
│   ├── TEXT/       # Plain text files
│   └── XML/        # XML format files
├── word/           # Word-based tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── char/           # Character-based tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── grammar/        # Grammar-based tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── subword/        # Subword tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── subword_bpe/    # BPE tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── subword_syllable/ # Syllable tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
├── subword_frequency/ # Frequency tokenization
│   ├── JSON/
│   ├── CSV/
│   ├── TEXT/
│   └── XML/
└── byte/           # Byte tokenization
    ├── JSON/
    ├── CSV/
    ├── TEXT/
    └── XML/
```

## 📄 File Naming Convention

Files are automatically named with the following pattern:
- **JSON**: `tokenization-{tokenizer_type}-{date}.json`
- **CSV**: `tokenization-{tokenizer_type}-{date}.csv`
- **TEXT**: `tokenization-{tokenizer_type}-{date}.txt`
- **XML**: `tokenization-{tokenizer_type}-{date}.xml`
- **Decoded**: `decoded-text-{tokenizer_type}-{date}.txt`

## 🎯 Benefits

1. **Organized**: All outputs are neatly organized by tokenizer type
2. **Multiple Formats**: Support for JSON, CSV, TEXT, and XML formats
3. **Easy Navigation**: Clear folder structure for quick access
4. **Automatic Naming**: Files are automatically named with timestamps
5. **No Clutter**: No more random files scattered around

## 🔧 Usage

When you download tokenization results from the SOMA interface:
1. Files are automatically saved to the appropriate folder
2. JSON files go to `{tokenizer_type}/JSON/`
3. CSV files go to `{tokenizer_type}/CSV/`
4. TEXT files go to `{tokenizer_type}/TEXT/`
5. XML files go to `{tokenizer_type}/XML/`

## 📊 Supported Tokenizer Types

- **space**: Space-based tokenization
- **word**: Word-based tokenization  
- **char**: Character-based tokenization
- **grammar**: Grammar-based tokenization
- **subword**: Subword tokenization
- **subword_bpe**: BPE tokenization
- **subword_syllable**: Syllable tokenization
- **subword_frequency**: Frequency tokenization
- **byte**: Byte tokenization

## 🚀 Getting Started

1. Run tokenization in the SOMA interface
2. Click any download button (JSON, CSV, TEXT, XML)
3. Files will be automatically saved to the correct folder
4. Navigate to the appropriate folder to find your files

---

**Note**: This organized system ensures all your tokenization outputs are properly categorized and easy to find!
