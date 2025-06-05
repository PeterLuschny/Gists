# A Guide to b-files in the OEIS

This document explains what b-files are, describes their strict and loose formats, and provides guidelines on how they should be produced and submitted.

---

## 1. Overview

**What is a b-file?**  
A *b-file* is a plain-text document used by the On-Line Encyclopedia of Integer Sequences (OEIS) to supply many more terms of a sequence than those shown in the main sequence entry. While b-files are defined by a context‐sensitive language, in practice they are easy to verify using simple automata. They tend to contain thousands or even tens of thousands of terms (or, in some cases, hundreds of thousands).

---

## 2. Strict b-file Format

### 2.1 File Encoding and Naming

- **Encoding:**  
  - Files are encoded in UTF-8 using only the ASCII subset (i.e., only ASCII printable characters are allowed as well as the line feed control character, U+000A).  
  - A Unicode byte-order mark (BOM, EF BB BF) is **not** allowed.
  
- **Filename:**  
  - The filename is formed by the letter “b” followed by the numeric part of the sequence’s A-number and the extension `.txt`.  
  - **Example:** The file for A000040 (the primes) is named `b000040.txt`.

### 2.2 Line Structure and Allowed Content

Each line in a strict b-file must be one of the following:

- **Content Lines:**  
  - Formatted as `n a(n)`, where `n` is the index and `a(n)` is the sequence term.  
  - **Format details:**  
    - A content line consists of a number, a single space (Unicode U+0020), and another number.  
    - A valid number is either:
      - A digit (1–9) followed by zero or more digits (0–9), or
      - A minus sign (`-`, U+002D) followed by a digit pattern as above, or
      - The single digit `0`.
    - Lines must terminate with a Unix-style linefeed (LF, U+000A). The very last line must also have a terminating linefeed, or the server may miscount the number of entries.
  
- **Comment Lines:**  
  - Start with the `#` character. (A comment line might begin with `# ` followed by additional text.)  
  - Comments can include timestamps, literature sources, or even excerpts of source code.
  
- **Blank Lines:**  
  - Empty lines (or lines with only whitespace) are allowed but generally discouraged, especially at the beginning of the file.

### 2.3 Order and Index Rules

- The indices (the first numbers in content lines) must be consecutive:
  - Either each index is exactly one **larger** than the previous non-comment, non-blank line, **or**
  - Each index is exactly one **smaller** than the previous.
- The very first index must equal the sequence’s offset (as given in the sequence entry).
- **Remarks for complete sequences:**  
  - When a b-file contains all terms of a finite sequence, the corresponding entry is marked with “(complete sequence)” and includes the keyword `full`.

### 2.4 Additional Constraints

- **Line Length:** Lines should not generally exceed 1000 characters to ensure compatibility with all tools.
- **Number Size:** It is strongly recommended that the numbers in content lines do not exceed 1000 digits.
- **Formatting:**  
  - Use spaces (not tabs) to separate entries.  
  - b-file lines must be contiguous and free from extraneous whitespace.
  
---

## 3. Loose b-file Format

Some b-files may not strictly follow the rules above but can be automatically converted. The loose format accepts additional variations:

### 3.1 Recognizing Variations

- **Content Lines (loose):**  
  They might match a pattern like:  
  ```
  ^\s*((?:[-\x2212]?[1-9][0-9]*)|0)\s+((?:-?[1-9][0-9]*)|0)\s*(#.*)?$
  ```
  Here, whitespace around the numbers and inline comments (beginning with `#`) is allowed.
  
- **Comment Lines (loose):**  
  Lines with leading whitespace followed by `#` are treated as comments:
  ```
  ^\s*#
  ```
  
- **Blank Lines (loose):**  
  Blank or whitespace-only lines match:
  ```
  ^\s*$
  ```

### 3.2 Conversion Process

To convert a loose b-file to strict format:

1. **Normalize Line Terminators:**  
   Replace carriage returns (`U+000D`) or CR-LF combinations with a single linefeed (LF, U+000A).

2. **Trim Whitespace:**  
   - Remove any leading or trailing whitespace in content lines.
   - Replace sequences of internal whitespace in content lines with a single space.
   - In comment lines, remove whitespace before the `#` character.

3. **Move Inline Comments:**  
   If a content line includes an inline comment (after the data), move the comment to a separate line (either before or after the content line).

4. **Character Normalization:**  
   - Replace non-standard minus signs (Unicode U+2212) with the hyphen-minus (U+002D).
   - Replace occurrences of “-0” with “0” in content lines.

---

## 4. Using and Generating b-files

- **Purpose:**  
  b-files typically contain many more terms than what is displayed in the main sequence entry. For example, while a typical sequence entry might show only the first 50–80 terms, a b-file might provide the first 1,000, 10,000, or even 100,000 terms.
  
- **Automatic Generation:**  
  If no b-file has been uploaded for a sequence, the server generates one containing exactly the terms shown in the sequence entry to facilitate automated processing.

- **Flattening Triangles and Arrays:**  
  For sequences representing triangles or arrays, b-files are produced by “flattening” the multidimensional data into a single enumeration order.

---

## 5. Detailed File Format Specifications

### 5.1 File Content Rules

- **Plain Text Requirements:**  
  b-files contain only ASCII printable characters and the LF control character. Characters in the ANSI range (128–255) or Unicode code points above U+007E are not allowed.
  
- **Content Line Example:**  
  For A000040 (the primes), an excerpt might look like:
  ```
  1 2
  2 3
  3 5
  4 7
  ...
  9998 104717
  9999 104723
  10000 104729
  ```
  There is no extra space before the index; a single space separates the index from the term.
  
### 5.2 Comment Insertion

- Comments may be interleaved with content lines for explanatory notes such as:
  - Creation time stamps.
  - Literature or source references.
  - Program source code (if too lengthy for the database entry).

---

## 6. Contributing a b-file to the OEIS

### 6.1 Upload Guidelines

- When uploading a b-file:
  - **Create a Link:**  
    Ensure that you add a link to the file in the sequence entry; otherwise, the file will not be visible.
  
  - **Template Assistance:**  
    A template is provided when editing a sequence, which automatically fills in the MIN and MAX (minimum and maximum term values).
  
  - **Consistency Checks:**  
    You will receive warnings if the b-file does not match the existing sequence data (including mismatches in the offset).

### 6.2 Formatting and Extension Instructions

- **Each Pair on a Single Line:**  
  Even if a sequence term is very large, it must remain on one line.
  
- **No Tabs, Use Spaces:**  
  Use spaces rather than tabs between the index and the term.
  
- **File Size Limit:**  
  There is an approximate 10-megabyte limit on the file size. Files exceeding this size may be truncated without warning.

- **Contributing to an Existing b-file:**  
  If you extend a b-file with additional terms, update the author’s name to include your contribution and add a comment detailing which term ranges were provided by which contributors.  
  **Example:**  
  ```
  Lars Blomberg, Table of n, a(n) for n=1..12000
  (terms 1–500 from Jon E. Schoenfield, terms 501–1000 from Chai Wah Wu)
  ```

### 6.3 Submission Reminders

- **Offset Verification:**  
  Ensure that the first index in the content lines matches the offset listed in the sequence entry.
  
- **Final Blank Line:**  
  Always end the file with a blank (empty) line. Failing to do so may cause the last data line to be ignored.
  
- **Editing Tools:**  
  The OEIS system automatically converts non-Unix text files (e.g., converting tab characters to spaces and changing CR-LF to LF).

---

## 7. Final Remarks

- **Strict adherence to the b-file format is important** to ensure that all automated tools and parsing software can accurately read and process the data.
- **Take care with the ordering and formatting**—each content line must follow the prescribed format and order, and numbers should not be excessively long.
- **For sequences represented by triangles or arrays**, remember that the submitted b-file is a flattened version determined by a specific serialization order.

By following these guidelines, contributors can ensure that their b-files are consistent, accurately represent the sequence data, and can be reliably processed by OEIS systems and associated tools.

---
