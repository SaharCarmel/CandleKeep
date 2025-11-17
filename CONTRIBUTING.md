# Contributing to Sahar's Claude Code Marketplace

This marketplace is currently a **private personal collection** maintained by Sahar Carmel. However, if you'd like to suggest plugins or improvements, here's how the process works.

## Suggesting Plugins

If you know of a great Claude Code plugin that should be added:

1. Open an issue with:
   - Plugin name
   - Repository URL
   - Brief description of what it does
   - Why it would be valuable

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
- Solve a real problem or add meaningful value
- Not duplicate existing plugins (unless significantly better)
- Work reliably in common use cases

## Adding Plugins (Maintainer Guide)

### Manual Method

1. Edit `.claude-plugin/marketplace.json`
2. Add plugin entry with all required fields:
   ```json
   {
     "name": "plugin-name",
     "description": "What it does",
     "version": "1.0.0",
     "author": "Author Name",
     "license": "MIT",
     "source": {
       "type": "github",
       "repo": "owner/repo"
     }
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

## Version Management

When updating an existing plugin's version:

1. Update the `version` field in marketplace.json
2. Test the new version locally
3. Note any breaking changes in commit message
4. Push update

## Questions?

Open an issue for any questions about contributing or using this marketplace.

---

*This is a living document and may evolve as the marketplace grows.*
