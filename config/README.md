To properly configure the project, follow these steps:

**Each configuration folder should have a `config.toml` file with the following contents**

**Set the `client_secrets_file` Path:**

* Ensure that the client_secrets_file entry in the config.toml file points to the correct path where your downloaded Google OAuth 2.0 credentials file is stored.

**Configure the `redirect_url`:**

* When creating the OAuth 2.0 credentials in the Google Cloud Console, make sure to include the redirect_url in the Authorized redirect URIs section.
The redirect_url should always correspond to the auth page of this project.