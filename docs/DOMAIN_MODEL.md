# Domain Model

## Purpose

This document defines the core language of A11yDaily.

The goal is to make sure the product, database, API, user interface, and documentation all use the same terms consistently.

## Core Principle

A11yDaily is not built around articles, feeds, or posts.

A11yDaily is built around knowledge.

## Core Entities

### Knowledge Asset

A Knowledge Asset is one public piece of information collected by A11yDaily.

Examples include:

- News article
- Blog post
- Government update
- Legal decision
- Standards update
- GitHub release
- YouTube video
- Webinar
- Podcast episode
- Research paper
- PDF guidance
- Document accessibility resource

### Source

A Source is a public location where Knowledge Assets are discovered.

Examples:

- W3C blog
- DOJ website
- WebAIM blog
- PDF Association website
- Adobe Accessibility resources

### Organization

An Organization is the entity responsible for a Source or Knowledge Asset.

Examples:

- W3C
- DOJ
- WebAIM
- PDF Association
- Adobe
- Microsoft

### Topic

A Topic is a subject that Knowledge Assets can relate to.

Examples:

- WCAG
- ARIA
- PDF/UA
- ADA Title II
- Section 508
- Document accessibility
- AI accessibility
- Forms
- Assistive technology

### Story

A Story is a group of related Knowledge Assets about the same event, issue, or development.

Example:

A DOJ rule update may include:

- Government announcement
- Legal analysis
- Accessibility blog response
- Webinar
- Community discussion

### Collection

A Collection is a user-curated group of Knowledge Assets.

Examples:

- PDF/UA research
- ADA Title II resources
- Higher education compliance
- Accessible documents training

### Daily Brief

A Daily Brief is a generated summary of important Knowledge Assets and Stories for a given time period.

## First-Class Domains

A11yDaily treats these domains as first-class areas of intelligence:

- Web accessibility
- Document accessibility
- PDF accessibility
- Mobile accessibility
- Legal and policy
- Standards and specifications
- Tools and testing
- AI and accessibility
- Education and research
- Community and events

## Naming Decision

For now, the canonical term is:

**Knowledge Asset**

Do not use these as core model names:

- Article
- Feed Item
- RSS Item
- Post

Those are source-specific formats, not platform concepts.

## Related Documents

- VISION.md
- CONSTITUTION.md
- ARCHITECTURE.md
- DATABASE.md
- SOURCES.md
