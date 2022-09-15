# sqlfmt

sqlfmt formats your dbt SQL files so you don't have to. It is similar in nature to black, gofmt, and rustfmt (but for SQL). 

1. **sqlfmt promotes collaboration.** An auto-formatter makes it easier to collaborate with your team and solicit contributions from new people. You will never have to mention (or argue about) code style in code reviews again.
2. **sqlfmt is fast.** Forget about formatting your code, and spend your time on business logic instead. sqlfmt processes hundreds of files per second and only operates on files that have changed since the last run.
3. **sqlfmt works with Jinja.** It formats the code that users look at, and therefore doesn't need to know anything about what happens after the templates are rendered.
3. **sqlfmt integrates with your workflow.** As a CLI written in Python, it's easy to install locally on any OS and run in CI. Plays well with dbt, pre-commit, SQLFluff, VSCode, and GitHub Actions.

## Using the sqlfmt CLI

[Read the docs](https://docs.sqlfmt.com/category/getting-started) to get started.

**tl;dr: `pip install shandy-sqlfmt[jinjafmt]`**

## Or you can try it out here

Type or paste SQL into the box below, then click the **sqlfmt!** button to see your code in the sqlfmt style.
