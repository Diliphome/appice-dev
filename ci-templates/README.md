# SDK doc-generator CI workflows

These four workflows live **in the SDK repos**, not in the `appice-dev` repo. Each one:

1. Runs the SDK's native doc generator (Apple DocC, Dokka, TypeDoc) on every release tag (`v*`).
2. Checks out the `appice-dev` portal repo with a fine-grained PAT.
3. Replaces the relevant `sdk/<platform>/reference/` folder with the freshly-generated HTML.
4. Commits and pushes back to `main` of `appice-dev`.
5. Netlify auto-deploys `dev.appice.ai` within ~60 seconds.

## Where each file goes

| File | Target SDK repo | Place at |
|---|---|---|
| `build-ios-docs.yml` | `appice-ios` | `.github/workflows/build-ios-docs.yml` |
| `build-android-docs.yml` | `appice-android` | `.github/workflows/build-android-docs.yml` |
| `build-web-docs.yml` | `appice-web` | `.github/workflows/build-web-docs.yml` |
| `build-rn-docs.yml` | `appice-react-native` | `.github/workflows/build-rn-docs.yml` |

## One-time setup

For each SDK repo:

1. **Generate a PAT** (fine-grained, scoped to *only* `Diliphome/appice-dev`, with `Contents: write` permission). One PAT per SDK repo is fine, or one shared.
2. **Add it as a secret** in the SDK repo's settings: `Settings → Secrets and variables → Actions → New repository secret` → name `APPICE_DEV_PUSH_TOKEN`.
3. **Verify the doc generator works locally** before pushing the workflow:
   - iOS: `xcodebuild docbuild -scheme Appice -derivedDataPath ./.derivedData -destination 'generic/platform=iOS Simulator'`
   - Android: `./gradlew :appice-android:dokkaHtml`
   - Web/RN: `npx typedoc`
4. **Tag a test release** (`v5.0.0-test1`) — the workflow will run, build docs, and commit them to the dev portal. Verify they appear at the right path.

## Initial backfill (manual, one time)

Until you tag a release, the `sdk/<platform>/reference/` folders in `appice-dev` are empty. To pre-populate:

```bash
# in each SDK repo
xcodebuild docbuild ...                      # iOS
# OR
./gradlew :appice-android:dokkaHtml          # Android
# OR
npx typedoc                                  # Web / RN

# copy output into the appice-dev repo:
cp -R <docs-output>/* /path/to/appice-dev/sdk/<platform>/reference/
cd /path/to/appice-dev
git add sdk/<platform>/reference
git commit -m "Initial backfill: <platform> SDK reference"
git push
```

After the first manual backfill, every release-tag push will keep the reference up to date automatically.
