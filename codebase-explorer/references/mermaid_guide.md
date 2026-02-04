# Mermaid Chart Guide

Quick reference for creating Mermaid diagrams in codebase documentation.

---

## Table of Contents
- [Flowchart](#flowchart)
- [Sequence Diagram](#sequence-diagram)
- [Graph (Tree) Diagram](#graph-tree-diagram)
- [Class Diagram](#class-diagram)
- [State Diagram](#state-diagram)
- [Best Practices](#best-practices)

---

## Flowchart

Use for: Process flows, decision trees, data flow, algorithm visualization

### Syntax

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
```

### Direction Options
- `TD` - Top to Down (default)
- `LR` - Left to Right
- `BT` - Bottom to Top
- `RL` - Right to Left

### Node Shapes
```mermaid
flowchart LR
    A[Rectangle] --> B(Rounded)
    B --> C([Stadium])
    C --> D((Circle))
    D --> E{Diamond}
    E --> F[/Parallelogram/]
    F --> G[\Parallelogram\]
```

### Styling
```mermaid
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
```

### Subgraphs
```mermaid
flowchart TD
    subgraph Frontend
        A[UI] --> B[Components]
    end

    subgraph Backend
        C[API] --> D[Database]
    end

    B --> C
```

---

## Sequence Diagram

Use for: API calls, function invocations, interaction sequences, request/response flows

### Syntax

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Server
    participant Database

    User->>Client: Request
    Client->>Server: API Call
    Server->>Database: Query
    Database-->>Server: Results
    Server-->>Client: Response
    Client-->>User: Display
```

### Message Types
- `->>` Synchronous message (solid line)
- `-->>` Return message (dotted line)
- `->` Asynchronous message (open arrow)
- `-->` Async return message

### Loops and Conditions
```mermaid
sequenceDiagram
    participant A
    participant B

    loop Check condition
        A->>B: Request
        B-->>A: Response
    end

    alt Success
        A->>A: Handle success
    else Error
        A->>A: Handle error
    end
```

### Activations
```mermaid
sequenceDiagram
    participant A
    participant B

    A->>+B: Request
    B-->>-A: Response
```

---

## Graph (Tree) Diagram

Use for: Directory structures, hierarchies, organization charts, dependency trees

### Syntax

```mermaid
graph TD
    Root[Project Root]
    Root --> Src[src/]
    Root --> Tests[tests/]
    Root --> Package[package.json]

    Src --> Components[components/]
    Src --> Pages[pages/]
    Src --> Utils[utils/]

    Components --> Header[Header.jsx]
    Components --> Footer[Footer.jsx]

    Pages --> Home[Home.jsx]
    Pages --> About[About.jsx]
```

### Styling for Directory Trees
```mermaid
graph TD
    Root[my-project/]
    Root --> Src[src/]
    Root --> Package[package.json]

    style Root fill:#e1f5ff,stroke:#333
    style Src fill:#fff4e1,stroke:#333
    style Package fill:#e8f5e9,stroke:#333
```

---

## Class Diagram

Use for: Data models, class relationships, database schemas, API structures

### Syntax

```mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }

    class Order {
        +String id
        +Date createdAt
        +Float total
        +addItem()
        +removeItem()
    }

    User "1" --> "*" Order : places
```

### Relationship Types
- `-->` Association
- `-->` Inheritance
- `-->` Composition
- `-->` Aggregation
- `-->` Dependency

### Example with Multiple Relationships
```mermaid
classDiagram
    class User {
        +id: String
        +name: String
        +email: String
    }

    class Post {
        +id: String
        +title: String
        +content: String
    }

    class Comment {
        +id: String
        +text: String
    }

    User "1" --> "*" Post : creates
    Post "1" --> "*" Comment : has
    User "1" --> "*" Comment : writes
```

---

## State Diagram

Use for: State machines, workflow states, application lifecycles, component states

### Syntax

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start
    Processing --> Success: Complete
    Processing --> Error: Fail
    Success --> [*]
    Error --> Idle: Retry
```

### Composite States
```mermaid
stateDiagram-v2
    [*] --> NotRunning

    state Running {
        [*] --> Active
        Active --> Paused
        Paused --> Active
    }

    NotRunning --> Running: Start
    Running --> NotRunning: Stop
```

---

## Best Practices

### 1. Keep Diagrams Simple
- Avoid too many nodes (aim for < 20)
- Use clear, concise labels
- Focus on the essential flow

### 2. Use Consistent Naming
- Use verb-noun format for actions (e.g., "Load Data")
- Use noun phrases for states (e.g., "Processing")
- Be specific but not verbose

### 3. Color Coding
```mermaid
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]

    %% Color scheme
    classDef start fill:#4CAF50,stroke:#333,stroke-width:2px,color:white
    classDef process fill:#2196F3,stroke:#333,stroke-width:2px,color:white
    classDef end fill:#f44336,stroke:#333,stroke-width:2px,color:white

    class A start
    class B process
    class C end
```

### 4. Use Subgraphs for Organization
```mermaid
flowchart TD
    subgraph Frontend
        A[React App]
        B[Components]
    end

    subgraph Backend
        C[API Server]
        D[Database]
    end

    A --> C
    B --> C
    C --> D
```

### 5. Add Legends When Needed
```
Legend:
- Solid arrows: Direct calls
- Dotted arrows: Data flow
- Green nodes: Success states
- Red nodes: Error states
```

### 6. Document Complex Flows
For complex flows, break into multiple diagrams:
1. High-level overview
2. Detailed subprocess
3. Error handling flow

---

## Common Diagrams for Codebase Analysis

### Application Architecture
```mermaid
flowchart TB
    subgraph Frontend
        UI[User Interface]
        Components[React Components]
    end

    subgraph Backend
        API[REST API]
        Services[Business Logic]
        DB[(Database)]
    end

    UI --> Components
    Components --> API
    API --> Services
    Services --> DB
```

### Request Flow
```mermaid
sequenceDiagram
    participant Client
    participant Router
    participant Controller
    participant Service
    participant Database

    Client->>Router: HTTP Request
    Router->>Controller: Route Match
    Controller->>Service: Business Logic
    Service->>Database: Query
    Database-->>Service: Data
    Service-->>Controller: Result
    Controller-->>Client: HTTP Response
```

### Module Dependencies
```mermaid
graph TD
    App[Main App] --> Auth[Auth Module]
    App --> Users[Users Module]
    App --> API[API Gateway]

    Auth --> DB[(Database)]
    Users --> DB
    API --> Auth
    API --> Users

    style App fill:#f9f,stroke:#333
    style DB fill:#bbf,stroke:#333
```

### Data Flow
```mermaid
flowchart LR
    Input[User Input] --> Validate[Validation]
    Validate --> Process[Processing]
    Process --> Store[Storage]
    Store --> Display[Display]

    style Input fill:#e1f5ff
    style Display fill:#e8f5e9
```

---

## Tips for Codebase Documentation

1. **Start with high-level diagrams** before diving into details
2. **Use consistent styling** across all diagrams in the document
3. **Include file paths** as labels where helpful
4. **Highlight key files** with distinctive colors
5. **Add comments** for complex logic or decisions
6. **Keep diagrams readable** - test at different zoom levels

---

## Mermaid Resources

- [Official Documentation](https://mermaid.js.org/intro/)
- [Live Editor](https://mermaid.live/)
- [Syntax Examples](https://mermaid.js.org/syntax/examples.html)
