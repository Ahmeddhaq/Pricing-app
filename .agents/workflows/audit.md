---
description: 
---

# /audit

## Description
Run a comprehensive codebase audit using the security audit skill.

## Instructions
1. Activate the `security-audit` skill
2. Scan the entire codebase systematically
3. Follow the audit checklist in the skill
4. Generate a detailed report following this format:
   - Executive Summary
   - Critical Issues (Must Fix Now)
   - High Priority Issues (Fix Soon)
   - Medium Priority Issues (Fix when possible)
   - Low Priority / Recommendations
   - Dead Code / Files to Delete
   - Files to Review

## Output
**CRITICAL**: Save the final report to `specs/audit/report.md`
- Use markdown formatting
- Include file paths and line numbers
- Provide specific remediation steps
- Include a health score out of 100

## After Saving
Tell the user: "Audit report saved to specs/audit/report.md. Review it and run `/audit-fix` to start fixing issues."