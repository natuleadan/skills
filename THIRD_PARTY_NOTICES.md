# Third Party Notices

The skills themselves contain no third-party code: they are instructions and
prose. The repository uses the following development dependencies, all under the
MIT license. They are build and validation tooling and are not part of the
published skill content.

## Changesets

- Packages: `@changesets/cli`, `@changesets/changelog-github`
- Repository: https://github.com/changesets/changesets
- License: MIT
- Used for: versioning and changelog generation

## commitlint

- Packages: `@commitlint/cli`, `@commitlint/config-conventional`
- Repository: https://github.com/conventional-changelog/commitlint
- License: MIT
- Used for: commit message validation

## Husky

- Package: `husky`
- Repository: https://github.com/typicode/husky
- License: MIT
- Used for: local git hooks

## GitHub Actions

- Actions: `actions/checkout`, `actions/setup-node`, `pnpm/action-setup`,
  `softprops/action-gh-release`
- License: MIT
- Used for: continuous integration and releases

---

The MIT license text applies to the packages listed above. All other content in
this repository is original and licensed under the Apache License 2.0; see
[LICENSE](LICENSE) and [NOTICE](NOTICE).
