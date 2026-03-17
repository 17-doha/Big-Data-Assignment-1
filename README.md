# The Digital Librarian: Distributed Reverse Indexing 

This repository contains the source code and configuration files for a **Fully Distributed Hadoop 3.2.1 Inverted (Reverse) Index Pipeline**. The project uses a containerized Apache Hadoop cluster (managed via Docker Compose) to process large text corpora and build a reverse index mapping words to the documents they appear in, along with their frequencies.

The MapReduce logic is implemented in **Python 3** using the Hadoop Streaming API and relies on the **NLTK** library for natural language processing (tokenization and stemming).

---

## 📁 Repository Structure

- `docker-compose.yml`: Defines the 6-container Hadoop cluster (NameNode, ResourceManager, and 4 DataNode/NodeManager pairs).
- `mapper.py`: Reads text, tokenizes, removes stop-words, stems words, and emits `(word,doc_id) -> 1`.
- `combiner.py`: Performs local aggregation on map outputs to reduce network shuffle traffic.
- `reducer.py`: Aggregates global counts and formats the final inverted index string.
- `stopwords.txt`: A list of common words filtered out during the Map phase.
- `run_project.sh`: The master execution script that automates HDFS ingestion, job submission, and performance timing.

---

## Prerequisites

Before running the pipeline, ensure your host machine has the following installed:

- **Docker**
- **Docker Compose**

You will also need a dataset of text documents. Place your text files (e.g., `.txt` books) into your host machine's `~/Downloads/books` folder. This folder is volume-mapped to `/workspace/books` inside the Docker containers.

---

##  Setup & Initialization

### 1. Start the Hadoop Cluster

```bash
docker-compose down --remove-orphans
docker-compose up -d
```

Wait about **10–15 seconds** to ensure all nodes have properly initialized.

---

### 2. Enter the NameNode

```bash
docker exec -it namenode /bin/bash
```

---

### 3. Install Container Dependencies

```bash
# Fix Debian repository links
echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

# Install Python & Pip
apt-get update
apt-get install -y python3 python3-pip

# Install NLTK
pip3 install setuptools nltk==3.4.5
python3 -c "import nltk; nltk.download('punkt')"
```

---

## ⚙️ Execution

```bash
chmod +x /workspace/run_project.sh
/workspace/run_project.sh
```

---

### What `run_project.sh` Does

- Cleans up any previous runs in HDFS (`/user/student/library` and `/user/student/final_index_output`)
- Creates the HDFS directories and uploads local text files from `/workspace/books/`
- Triggers the Hadoop Streaming MapReduce job
- Calculates and prints total execution time
- Prints the top 20 index entries to the console

---

## Sample Output Format

```plaintext
hadoop    book1.txt,12 book3.txt,5
data      book2.txt,8 book1.txt,2
```
