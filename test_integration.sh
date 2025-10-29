#!/bin/bash
# Test integration script for Corpaxe scraper

echo "=== Testing Corpaxe Scraper Integration ==="
echo

# Test with a valid ticker
echo "Test 1: Valid ticker (AAPL)"
OUTPUT=$(/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "AAPL" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    SCREENSHOT=$(echo "$OUTPUT" | grep "^LAST_SCREENSHOT=" | cut -d'=' -f2)
    echo "✓ Success! Exit code: $EXIT_CODE"
    echo "✓ Screenshot: $SCREENSHOT"
    
    # Check if file exists
    if [ -f "$SCREENSHOT" ]; then
        echo "✓ Screenshot file exists"
    else
        echo "✗ Screenshot file not found"
    fi
else
    echo "✗ Failed with exit code: $EXIT_CODE"
fi

echo
echo "Test complete"
