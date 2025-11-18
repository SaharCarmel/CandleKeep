# Contributing to CandleKeep Marketplace

This marketplace is a **personal collection** maintained by Sahar Carmel, focused on knowledge infrastructure and tools for AI agents. However, suggestions and contributions are welcome!

## Suggesting Plugins

If you know of a great Claude Code plugin that fits the CandleKeep philosophy:

1. Open an issue with:
   - Plugin name
   - Repository URL
   - Brief description of what it does
   - Why it aligns with CandleKeep's knowledge-focused mission

2. I'll review and potentially add it to the marketplace

## Plugin Submission Guidelines

For a plugin to be considered for this marketplace, it should:

### Quality Standards
- Have clear, comprehensive documentation
- Follow Claude Code plugin best practices
- Be actively maintained
- Have a clear license

### Security Considerations
- No obvious security vulnerabilities
- Transparent about permissions required
- Trustworthy source (reputable author/organization)

### Functionality
- Solve a real problem related to knowledge management, learning, or AI agent enhancement
- Not duplicate existing plugins (unless significantly better)
- Work reliably in common use cases

### Alignment with CandleKeep Philosophy
- Enhance how AI agents access or use knowledge
- Support personalized learning and intelligence
- Focus on practical utility for knowledge workers

## Adding Plugins (Maintainer Guide)

### Manual Method

1. Edit `.claude-plugin/marketplace.json`
2. Add plugin entry with all required fields:
   ```json
   {
     "name": "plugin-name",
     "description": "What it does",
     "version": "1.0.0",
     "author": {
       "name": "Author Name",
       "email": "author@example.com"
     },
     "source": "./plugins/plugin-name",
     "category": "productivity",
     "keywords": ["relevant", "search", "terms"]
   }
   ```
3. Run validation: `./scripts/validate.sh`
4. Commit and push

### Using Helper Script

```bash
./scripts/add-plugin.sh
```

Follow the interactive prompts to add a new plugin.

## Testing New Plugins

Before adding to the marketplace:

1. Test the plugin locally in a Claude Code project
2. Verify all commands/features work as expected
3. Check documentation is accurate
4. Ensure no conflicts with other marketplace plugins
5. Validate security and permissions

## Version Management

When updating an existing plugin's version:

1. Update the `version` field in marketplace.json
2. Test the new version locally
3. Note any breaking changes in commit message
4. Push update

## Creating New Plugins

If you want to contribute a new plugin to CandleKeep:

1. Create your plugin following [Claude Code plugin guidelines](https://code.claude.com/docs/en/plugins)
2. Add it to the `plugins/` directory with:
   - `.claude-plugin/plugin.json` - Plugin metadata
   - `README.md` - Documentation
   - Source code and any necessary files
3. Update `.claude-plugin/marketplace.json`
4. Test thoroughly
5. Submit a pull request or open an issue

## Code of Conduct

- Be respectful and constructive in all interactions
- Focus on knowledge sharing and learning
- Prioritize quality over quantity
- Respect intellectual property and licenses

## Questions?

Open an issue for any questions about contributing or using this marketplace.

---

*This is a living document and may evolve as the marketplace grows.*
