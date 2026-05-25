# Install the Stripe CLI

Install the Stripe CLI on macOS, Windows, or Linux.

The Stripe CLI lets you build, test, and manage your integration from the command line. You can use the Stripe CLI to:

- Create, retrieve, update, or delete any of your Stripe resources in a test environment.
- Stream real-time API requests and events occurring on your account.
- Trigger events to test your webhook integration.

For more information, see the [Stripe CLI reference](https://docs.stripe.com/cli.md).
[Watch on YouTube](https://www.youtube.com/watch?v=iFwBGI-kqeE)
## Install the Stripe CLI

From the command line, use an install script or download and extract a versioned archive for your operating system to install the CLI.

#### homebrew

To install the Stripe CLI with [homebrew](https://brew.sh/), run the following command:

```bash
brew install stripe/stripe-cli/stripe
```

#### apt

The Debian build for the CLI is available on [JFrog](https://packages.stripe.dev), which is not a Stripe-owned domain. When you visit this URL, it will redirect to Jfrog's artifact listing.

To install the Stripe CLI on Ubuntu and Debian-based distributions:

1. Add the Stripe CLI GPG key to the apt keyring:

   ```bash
   curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg > /dev/null
   ```

1. Add the CLI apt repository to the apt sources list:

   ```bash
   echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
   ```

1. Update the package list:

   ```bash
   sudo apt update
   ```

1. Install the CLI:

   ```bash
   sudo apt install stripe
   ```

#### yum

The RPM build for the CLI is available on [JFrog](https://packages.stripe.dev), which is not a Stripe-owned domain. When you visit this URL, it will redirect to Jfrog's artifact listing.

To install the Stripe CLI on RPM-based distributions:

1. Add the CLI yum repository to the yum sources list:

   ```bash
   echo -e "[Stripe]\nname=stripe\nbaseurl=https://packages.stripe.dev/stripe-cli-rpm-local/\nenabled=1\ngpgcheck=0" >> /etc/yum.repos.d/stripe.repo
   ```

1. Install the CLI:

   ```bash
   sudo yum install stripe
   ```

#### Scoop

To install the Stripe CLI with [Scoop](https://scoop.sh/), run the following command:

```bash
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
```

```bash
scoop install stripe
```

#### macOS

To install the Stripe CLI on macOS without homebrew:

1. Download the latest `mac-os` tar.gz file for your CPU architecture type from [GitHub](https://github.com/stripe/stripe-cli/releases/latest).

1. Extract the file: `tar -xvf stripe_[X.X.X]_mac-os_[ARCH_TYPE].tar.gz`.

Optionally, you can install the binary in a location where you can run it globally (e.g., `/usr/local/bin`).

#### Linux

To install the Stripe CLI on Linux without a package manager:

1. Download the latest `linux` tar.gz file from [GitHub](https://github.com/stripe/stripe-cli/releases/latest).

1. Extract the file: `tar -xvf stripe_X.X.X_linux_x86_64.tar.gz`.

1. Move `./stripe` to your execution path.

#### Windows

To install the Stripe CLI on Windows without Scoop:

1. Download the latest `windows` ZIP file from [GitHub](https://github.com/stripe/stripe-cli/releases/latest).

1. Extract the `stripe_X.X.X_windows_x86_64.zip` file.

1. Add the path to the extracted `stripe.exe` file to the `Path` environment variable. For more information on updating environment variables, see the [Microsoft PowerShell documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.3#saving-changes-to-environment-variables).

Windows antivirus scanners occasionally flag the Stripe CLI as unsafe. This is most likely a false positive. For more information, see [Issue #692](https://github.com/stripe/stripe-cli/issues/692) in the GitHub repository.

#### Docker

The Stripe CLI is also available as a [Docker image](https://hub.docker.com/r/stripe/stripe-cli). To install the latest version, run the following command:

```bash
docker run --rm -it stripe/stripe-cli:latest
```

## Log in to the CLI

1. Sign in and authenticate your Stripe user [account](https://docs.stripe.com/get-started/account/activate.md) to generate a set of restricted keys. For more information, see [Stripe CLI keys and permissions](https://docs.stripe.com/stripe-cli/keys.md).

   ```bash
     stripe login
   ```

1. Press the **Enter** key on your keyboard to complete the authentication process in your browser.

   ```bash
   Your pairing code is: enjoy-enough-outwit-win
   This pairing code verifies your authentication with Stripe.
   Press Enter to open the browser or visit https://dashboard.stripe.com/stripecli/confirm_auth?t=THQdJfL3x12udFkNorJL8OF1iFlN8Az1 (^C to quit)
   ```

Optionally, if you don't want to use a browser, use the `--interactive` flag to authenticate with a restricted key or an existing API secret key. This is useful when authenticating the CLI without a browser, such as in a CI/CD pipeline.

```bash
stripe login --interactive
```

You can also use the `--api-key` flag to specify your API secret key inline each time you send a request.

```bash
stripe login --api-key <<YOUR_SECRET_KEY>>
```
