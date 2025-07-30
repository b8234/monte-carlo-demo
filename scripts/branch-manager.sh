#!/bin/bash

# Branch Management Helper for Monte Carlo Demo
# =============================================

echo "🔀 Monte Carlo Demo - Branch Management Helper"
echo "=============================================="
echo

case "$1" in
    "merge-to-main")
        echo "📋 Merging main-staging to main (excluding personal.md)..."
        echo "⚠️  IMPORTANT: This will exclude personal.md from main branch"
        echo
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git checkout main
            git merge main-staging --no-commit
            git reset HEAD personal.md
            git checkout -- personal.md 2>/dev/null || true
            echo "✅ Ready to commit merge (personal.md excluded)"
            echo "💡 Run: git commit -m 'Merge main-staging (exclude personal.md)'"
        else
            echo "❌ Merge cancelled"
        fi
        ;;
    "status")
        echo "📊 Current Branch Status:"
        echo "========================"
        echo "Current branch: $(git branch --show-current)"
        echo
        echo "📁 Files in main-staging:"
        git ls-tree -r --name-only main-staging | grep -E "(personal\.md|README\.md|src/)" || echo "No key files found"
        echo
        echo "📁 Files in main:"
        git ls-tree -r --name-only main 2>/dev/null | grep -E "(personal\.md|README\.md|src/)" || echo "Main branch not found or no key files"
        ;;
    *)
        echo "📖 Usage:"
        echo "  $0 merge-to-main    # Merge main-staging to main (excluding personal.md)"
        echo "  $0 status          # Show current branch status"
        echo
        echo "📋 Branch Strategy:"
        echo "  • main-staging: Full development with personal.md included"
        echo "  • main: Clean production code without personal.md"
        echo "  • personal.md: Contains presentation guide (staging only)"
        ;;
esac
