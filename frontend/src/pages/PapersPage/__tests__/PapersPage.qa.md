# QA Testing Sheet: Papers Analysis Page

## Test Environment
- **URL**: http://localhost:3000/dashboard/papers
- **Tested By**: _______________
- **Date**: _______________
- **Browser**: _______________

---

## Test Cases

### 1. Page Load
- [ ] Page loads without errors
- [ ] Loading spinner appears during initial data fetch
- [ ] All charts render after data loads
- [ ] No console errors

**Expected**: Page loads smoothly with loading indicator, then displays charts

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 2. Yearly Chart
- [ ] Line chart displays with correct data
- [ ] X-axis shows years
- [ ] Y-axis shows publication counts
- [ ] Chart title is "Publications by Year"
- [ ] Data points are connected with lines
- [ ] Hovering shows tooltip with values

**Expected**: Line chart with yearly trends

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 3. Journal Chart
- [ ] Pie chart displays with correct data
- [ ] Legend shows journal grades (SCI, KCI, etc.)
- [ ] Chart title is "Publications by Journal Grade"
- [ ] Colors distinguish different grades
- [ ] Hovering shows tooltip with values
- [ ] Legend positioned on right side

**Expected**: Pie chart with journal distribution

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 4. Field Chart
- [ ] Bar chart displays with correct data
- [ ] X-axis shows department/field names
- [ ] Y-axis shows publication counts
- [ ] Chart title is "Publications by Field"
- [ ] Hovering shows tooltip with values

**Expected**: Bar chart with field statistics

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 5. Year Filter
- [ ] Year dropdown shows options (All Years, 2023, 2022, 2021, 2020)
- [ ] Selecting year triggers data refetch
- [ ] Loading spinner appears during refetch
- [ ] Charts update with filtered data
- [ ] Filter selection persists visually

**Expected**: Filter works correctly and updates all charts

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 6. Journal Filter
- [ ] Journal dropdown shows options (All Grades, SCI, KCI, SCOPUS, 기타)
- [ ] Selecting journal grade triggers data refetch
- [ ] Loading spinner appears during refetch
- [ ] Charts update with filtered data
- [ ] Filter selection persists visually

**Expected**: Filter works correctly and updates all charts

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 7. Field Filter
- [ ] Field dropdown shows options (All Fields, 공학, 의학, 자연과학, 인문학)
- [ ] Selecting field triggers data refetch
- [ ] Loading spinner appears during refetch
- [ ] Charts update with filtered data
- [ ] Filter selection persists visually

**Expected**: Filter works correctly and updates all charts

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 8. Multiple Filters
- [ ] Can select multiple filters at once
- [ ] Selecting second filter while first is active works correctly
- [ ] All filters combine with AND logic
- [ ] Charts show data matching all active filters
- [ ] Loading state during combined filter refetch

**Expected**: Multiple filters work together correctly

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 9. Clear Filters Button
- [ ] Button is disabled when no filters are active
- [ ] Button is enabled when at least one filter is active
- [ ] Clicking button resets all filters to default
- [ ] Charts refetch and show all data
- [ ] Loading spinner appears during refetch

**Expected**: Clear button resets all filters and shows all data

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 10. Empty State (No Data)
- [ ] When filters result in no data, message displays
- [ ] Message says "No data available"
- [ ] Charts show empty state instead of errors
- [ ] Clear filters button still works

**Expected**: Graceful empty state when no data matches filters

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 11. Error Handling - Network Error
**Setup**: Disconnect network or stop backend server

- [ ] Error banner appears with message
- [ ] Error message is user-friendly
- [ ] Retry button appears
- [ ] Clicking retry attempts to refetch data
- [ ] Charts are hidden during error state

**Expected**: Error banner with retry option

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 12. Error Handling - 401 Unauthorized
**Setup**: Manually expire session token or logout from another tab

- [ ] Error banner appears with "Session expired" message
- [ ] No retry button (since session is invalid)
- [ ] User is redirected to login page
- [ ] After login, can access page again

**Expected**: Auto-logout and redirect to login

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 13. Responsive Design - Desktop
**Setup**: Test on desktop screen (1920x1080)

- [ ] All charts fit on screen
- [ ] Filters are in one row
- [ ] Journal and Field charts side-by-side
- [ ] No horizontal scrolling
- [ ] Text is readable

**Expected**: Optimal layout for desktop

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 14. Responsive Design - Tablet
**Setup**: Test on tablet screen (768x1024)

- [ ] All charts visible
- [ ] Filters may wrap to 2 rows
- [ ] Journal and Field charts may stack
- [ ] No horizontal scrolling
- [ ] Text is readable

**Expected**: Responsive layout adapts to tablet

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 15. Responsive Design - Mobile
**Setup**: Test on mobile screen (375x667)

- [ ] All charts stack vertically
- [ ] Filters stack vertically
- [ ] No horizontal scrolling
- [ ] Text is readable
- [ ] Touch targets are adequate size

**Expected**: Mobile-friendly stacked layout

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 16. Performance
- [ ] Initial page load < 3 seconds
- [ ] Filter change response < 1 second
- [ ] Chart rendering smooth, no lag
- [ ] No memory leaks after multiple filter changes
- [ ] Browser remains responsive during data fetch

**Expected**: Fast and responsive performance

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

### 17. Accessibility
- [ ] Tab navigation works through filters
- [ ] Filter labels are clear
- [ ] Charts have descriptive titles
- [ ] Error messages are announced
- [ ] Contrast ratio is adequate

**Expected**: Page is accessible to screen readers and keyboard users

**Actual**: _______________

**Status**: ✅ PASS / ❌ FAIL

---

## Summary

**Total Tests**: 17
**Passed**: _____
**Failed**: _____
**Pass Rate**: _____%

## Issues Found

| Issue # | Description | Severity | Steps to Reproduce |
|---------|-------------|----------|-------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Notes

_______________________________________________________________

_______________________________________________________________

_______________________________________________________________
