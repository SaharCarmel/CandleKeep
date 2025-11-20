# CandleKeep

<p align="center">
  <img src="candlekeep-logo.png" alt="CandleKeep Logo" width="400"/>
</p>

> *A personal library that brings the wisdom of books to your AI agents*

[![Status](https://img.shields.io/badge/status-early%20development-orange)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## What is this?

CandleKeep is a knowledge base system that gives AI agents direct access to your books—not just their memories of them. Like the legendary library fortress it's named after, CandleKeep preserves and provides knowledge, but for the age of artificial intelligence.

This repository serves as both the home of the CandleKeep project and a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) for distributing CandleKeep and related knowledge infrastructure tools.

---

## The Problem

When we ask AI agents for help, they rely on what they learned during training—a snapshot of knowledge that grows more distant with each passing day. This creates several challenges:

**The Memory Limitation**: Just as you wouldn't ask a developer to code without access to documentation, we shouldn't expect agents to work optimally with only their training memory of books.

**The Code Analogy**: Developers using AI coding assistants know this intuitively—giving an agent access to your actual codebase produces vastly better results than relying on the agent to "remember" how libraries work from training time.

**Knowledge Shapes Decisions**: Your knowledge determines your actions. Ask an agent for investment advice without context, and you'll get generic results. But an agent with access to your library of value investing books will give fundamentally different advice than one working with crypto trading guides.

## The Solution

CandleKeep is your personal knowledge infrastructure for AI agents. It's not just a book storage system—it's a living library that learns from how you use it.

### Core Concepts

**Books as Context, Not Data**: CandleKeep treats books as source material that agents can reference, annotate, and connect—just like you would with your own library.

**Neurons That Fire Together, Wire Together**: CandleKeep tracks how you access different parts of books during work sessions. When you reference Chapter 3 of *Clean Code* while also consulting *Refactoring*, the system notes this connection. Over time, these patterns reveal insights unique to your knowledge journey.

**Personalized Intelligence**: Two people can have identical book collections but develop completely different insights based on how they use them. CandleKeep captures and amplifies your unique knowledge patterns.

**Knowledge Transfer Between Humans**: Power users can write "agent-optimized" books—guides specifically designed for AI consumption. Share your methodology for working with agents, your coding patterns, or your analytical frameworks with others by packaging your knowledge as books for their agents.

## Key Features

### Book Management
- **Add books** from various formats (PDF, EPUB, text)
- **Intelligent parsing** using docling and LLMs to extract structured content
- **Organize** your library with custom categorization

### Rich Annotations
- **Highlights** for important passages
- **Bookmarks** for quick reference
- **Notes** to capture your thoughts and insights
- **Cross-references** to link ideas across different books

### Connection Mapping
- Automatic tracking of which books and sections are accessed together
- Session-based association to identify patterns in your knowledge usage
- Emergent insight discovery from usage patterns

### Agent Integration
- **Claude Code plugin** for seamless integration
- **Guided skills** that teach agents how to use your library effectively
- **Contextual responses** shaped by your book collection

## Available Plugins

### candlekeep-cli

The core CandleKeep CLI provides a Python-based command-line interface for managing your personal knowledge base, with MySQL storage and Claude Code integration.

[See full documentation →](./plugins/candlekeep-cli/README.md)

### dnd-dm

A comprehensive D&D 5e Dungeon Master assistant that provides immersive gameplay features including campaign management, dice rolling, adventure book integration with CandleKeep, and AI-powered NPC voices using ElevenLabs.

[See full documentation →](./plugins/dnd-dm/README.md)

---

## Use Cases

### Personalized Financial Advice
- **Scenario**: You ask an agent for investment strategy advice
- **Without CandleKeep**: Generic advice based on common knowledge
- **With CandleKeep**:
  - Value investing library → Advice focused on fundamental analysis, long-term holds
  - Crypto trading library → Advice on DeFi, yield farming, volatility strategies
  - Options trading library → Advice on hedging, spreads, risk management

### Coding Methodology Transfer
- **Scenario**: A senior developer shares their agentic coding approach
- **Process**:
  1. Write an "agent book" documenting TDD with AI pair programming techniques
  2. Share with team members who add it to their CandleKeep libraries
  3. Their agents now code using the senior developer's proven patterns
- **Result**: Institutional knowledge transferred at scale

### Research & Cross-Referencing
- **Scenario**: Writing a paper on distributed systems
- **Workflow**: Reference *Designing Data-Intensive Applications*, *The Art of Scalability*, and various research papers
- **CandleKeep Advantage**:
  - Agents can pull relevant sections from all sources
  - Connection tracking shows which concepts you consistently link
  - Emerging patterns suggest novel connections you might explore

### Domain Expertise Building
- **Scenario**: Learning machine learning with agent assistance
- **Progression**:
  1. Add foundational texts (*Pattern Recognition*, *Deep Learning*)
  2. Add specialized books as you advance
  3. Your agent's responses evolve with your library
  4. Session tracking shows your learning path and knowledge gaps

---

## Using this Marketplace

To use CandleKeep plugins in your Claude Code projects:

**Add the marketplace (one-liner in Claude Code):**
```
/plugin marketplace add SaharCarmel/candlekeep
```

**Install plugins:**
```
/plugin install candlekeep-cli@candlekeep
/plugin install dnd-dm@candlekeep
```

Or browse all available plugins interactively:
```
/plugin
```

## Marketplace Information

This repository follows the [Claude Code marketplace structure](https://code.claude.com/docs/en/plugin-marketplaces). The catalog is defined in `.claude-plugin/marketplace.json`.

**Adding plugins:** Use `./scripts/add-plugin.sh` or edit the marketplace.json manually
**Validation:** Run `./scripts/validate.sh` to check configuration

Check `.claude-plugin/marketplace.json` for the complete plugin catalog.

---

## Why "CandleKeep"?

In Dungeons & Dragons lore, Candlekeep is a fortress library dedicated to the collection and preservation of knowledge. It's a place where seekers of wisdom come to learn, researchers come to discover, and knowledge is treated as sacred. Our CandleKeep aspires to the same principle: creating a sanctuary for knowledge in the age of artificial intelligence, where wisdom isn't just stored—it's actively used, connected, and amplified.

---

## Project Status

**Early Development** - CandleKeep is currently in active development. The architecture is being refined, and the MVP features are being implemented. We welcome feedback, ideas, and contributions.

### Contributing

Interested in contributing? While we're still in early stages, we'd love to hear from:
- Developers interested in agent tooling
- Researchers exploring knowledge representation
- Power users of AI coding assistants
- Anyone passionate about books and AI

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

*Built with the belief that knowledge, when properly organized and accessed, reveals insights greater than the sum of its parts.*
