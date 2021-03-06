## 7.4.0 ##
Made Unite actions `add` and `delete` suitable for multiple selection

## 7.2.0 ##
Add `ProHistoryFileBrowse` that shows only diffs for the current file

## 7.1.0 ##
rename `:Projects` action `remove` to `delete` to match the native action, now
the `d` mapping works out of the box

## 6.3.0 ##
remove `libgit2` dependency

## 6.0.0 ##
Unite sources and kinds for addable projects and current projects

## 5.4.0 ##
Add `ProClone` command that creates a new project from a git repo

## 5.3.0 ##
Allow specifying only the project name to `ProAdd`, defaulting to the main
project's type

## 5.2.0 ##
Added completion for `ProTo`, `ProAdd` and `ProRemove`
## 5.0.0 ##
Added history browse mappings for reverting single commits

## 4.0.0 ##
Added the ability to checkout history states by cycling via
`ProHistory{Prev,Next}` and browsing in a scratch buffer via `ProHistoryBrowse`
