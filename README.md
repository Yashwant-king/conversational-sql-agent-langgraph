# Conversational SQL Agent with LangGraph

A conversational SQL agent built with **LangGraph, LangChain, LLMs, SQLAlchemy, and Microsoft SQL Server**.

The agent converts natural-language questions into SQL queries, validates the generated SQL, routes the request according to the SQL operation, and executes it against a SQL Server database.

For database-changing operations such as `INSERT`, `UPDATE`, and `DELETE`, the system uses **human approval before execution**.

---

## Features

- Natural language → SQL generation
- Dynamic database schema extraction
- SQL operation detection
- Conditional routing with LangGraph
- `SELECT` execution
- `INSERT` execution
- `UPDATE` execution
- `DELETE` execution
- Human approval for database-changing operations
- Retry limit for cyclic SQL-generation flow
- SQL Server integration using SQLAlchemy and PyODBC
- Structured LLM output for SQL-related question detection
- LangGraph state-based workflow

---

## Architecture

```text
                    User Question
                          |
                          v
                 +----------------+
                 |  Schema Node   |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 | SQL Relevance  |
                 |     Check      |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 |   Query Node   |
                 | Natural -> SQL |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 | Validate SQL   |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 | Operation      |
                 |    Router      |
                 +-------+--------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       SELECT          INSERT        UPDATE/DELETE
          |              |              |
          v              +------+-------+
      Execute                   |
          |                Human Approval
          |                   |
          |                   v
          |               Execute
          |                   |
          +---------+---------+
                    |
                    v
                   END