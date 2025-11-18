# Testing Strategy for CandleKeep

## Testing Philosophy

**CandleKeep uses ONLY end-to-end (E2E) testing.**

### What This Means

✅ **We DO:**
- Test complete user workflows via CLI commands
- Verify actual behavior users will experience
- Test database integration, file operations, and CLI output together
- Run all tests manually through Claude Code
- Document all test scenarios in task files

❌ **We DON'T:**
- Write unit tests for individual functions
- Create integration test suites
- Use testing frameworks (pytest, unittest, etc.)
- Mock databases or file systems
- Test components in isolation

### Rationale

1. **Simplicity**: CandleKeep is a straightforward CLI tool with clear workflows
2. **Real-world validation**: E2E tests catch issues that unit tests miss
3. **User-centric**: Tests verify what users actually experience
4. **Efficiency**: Less test code to maintain, faster iteration
5. **Claude Code integration**: All testing done by AI agent, not CI/CD

## How Testing Works

### Test Location
All testing procedures are documented in the relevant task file:
- `tasks/TASK001-cli-tool-book-management-metadata.md` contains 12 comprehensive E2E tests

### Test Execution
1. Claude Code reads the test procedures from task file
2. Executes each test scenario via actual CLI commands
3. Verifies output, files, and database state
4. Documents results in task progress log
5. Only marks task complete when ALL tests pass

### Test Environment
- Clean MySQL database for each major test run
- Fresh `~/.candlekeep/` directory (removed before testing)
- Real PDF and markdown sample files
- Actual MySQL server (not mocked)

## Test Coverage

### 12 E2E Test Scenarios

1. **Initial Setup** - Verify `candlekeep init` command
2. **Add PDF Book** - Test PDF parsing, metadata extraction, storage
3. **Add Markdown Book** - Test markdown parsing, frontmatter extraction
4. **Duplicate Detection** - Verify SHA256 hash prevents re-adding
5. **List Books** - Test filtering, formatting, sorting
6. **Show Book Details** - Verify complete metadata display
7. **Search Books** - Test full-text search functionality
8. **Library Statistics** - Verify aggregate statistics
9. **Update Metadata** - Test metadata modification
10. **Remove Book** - Test deletion with confirmation
11. **Error Handling** - Test all error scenarios gracefully
12. **Edge Cases** - Handle unusual but valid scenarios

### What Gets Tested

**Functionality:**
- All CLI commands work correctly
- Metadata extraction from PDFs and markdown
- Database operations (CRUD)
- File operations (read, write, copy, delete)
- Search and filtering
- Error handling

**User Experience:**
- Clear, helpful output messages
- Beautiful Rich formatting
- Progress indicators for long operations
- Confirmation prompts for destructive actions
- Helpful error messages with suggestions

**Data Integrity:**
- Correct metadata storage
- Proper file handling
- SHA256 deduplication
- Database constraints enforced
- No data loss on errors

## Success Criteria

A task is considered complete when:
1. ✅ All E2E tests pass without errors
2. ✅ CLI commands are intuitive and user-friendly
3. ✅ Error messages are clear and helpful
4. ✅ Rich formatting is consistent and beautiful
5. ✅ Performance is acceptable (<5s for most operations)
6. ✅ Documentation accurately reflects behavior

## Test Execution Example

```bash
# Test 1: Initial Setup
rm -rf ~/.candlekeep                    # Clean slate
candlekeep init                         # Run command
ls -la ~/.candlekeep/                   # Verify directories
cat ~/.candlekeep/config.yaml           # Verify config
mysql -e "SHOW TABLES FROM candlekeep;" # Verify database

# Test 2: Add PDF
candlekeep add-pdf ~/test.pdf --category "Tech"
ls ~/.candlekeep/library/               # Verify file created
mysql -e "SELECT * FROM candlekeep.books;" # Verify database

# ... and so on for all 12 tests
```

## Benefits of This Approach

**For Development:**
- Faster iteration (no test code to write/maintain)
- Focus on actual user experience
- Catch integration issues early
- Simple, clear test procedures

**For Quality:**
- Tests verify real-world usage
- Complete workflow validation
- Database, files, CLI tested together
- User experience is primary metric

**For Claude Code:**
- Clear, executable test procedures
- Easy to verify results
- Can run tests at any time
- Tests document expected behavior

## When to Run Tests

**During Development:**
- After completing each phase
- Before marking tasks as complete
- When fixing bugs
- After significant refactoring

**Test Frequency:**
- Phase completion: Run relevant tests
- Task completion: Run ALL tests
- Bug fix: Run affected tests + regression tests
- Major change: Full test suite

## Documenting Test Results

Test results are documented in the task file's progress log:

```markdown
### 2025-11-01
- Completed Phase 1 implementation
- Ran Test 1 (Initial Setup): ✅ PASS
  - Config file created correctly
  - Database schema created
  - All directories in place
- Ran Test 2 (Add PDF): ✅ PASS
  - Metadata extracted correctly
  - Markdown conversion successful
  - Database record created
```

## Important Notes

⚠️ **This is non-negotiable**: All testing for CandleKeep is E2E only.

✅ **This is intentional**: The simplicity of E2E-only testing matches the project scope.

📝 **This is documented**: Testing approach is in memory-bank, task files, and this document.

🤖 **This is Claude Code's responsibility**: All tests are run by the AI agent, not automated CI/CD.

---

For detailed test procedures, see: `tasks/TASK001-cli-tool-book-management-metadata.md`
