# Installation Script (Deprecated)

!!! note

    The installation script method is deprecated as of version 0.7. We recommend using Docker on Linux, and the [desktop installer](https://gpustack.ai/) on macOS or Windows.

## Linux and macOS

You can use the installation script available at `https://get.gpustack.ai` to install GPUStack as a service on systemd and launchd based systems.

You can set additional environment variables and CLI flags when running the script. The following are examples running the installation script with different configurations:

```bash
# Run server with the built-in worker.
curl -sfL https://get.gpustack.ai | sh -s -

# Run server with non-default port.
curl -sfL https://get.gpustack.ai | sh -s - --port 8080

# Run server with a custom data path.
curl -sfL https://get.gpustack.ai | sh -s - --data-dir /data/gpustack-data

# Run server without the built-in worker.
curl -sfL https://get.gpustack.ai | sh -s - --disable-worker

# Run server with TLS.
curl -sfL https://get.gpustack.ai | sh -s - --ssl-keyfile /path/to/keyfile --ssl-certfile /path/to/certfile

# Run server with external postgresql database.
curl -sfL https://get.gpustack.ai | sh -s - --database-url "postgresql://username:password@host:port/database_name"

# Run worker with specified IP.
curl -sfL https://get.gpustack.ai | sh -s - --server-url http://myserver --token mytoken --worker-ip 192.168.1.100

# Install with a custom PyPI mirror.
curl -sfL https://get.gpustack.ai | INSTALL_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple sh -s -

# Install a custom wheel package other than releases form pypi.org.
curl -sfL https://get.gpustack.ai | INSTALL_PACKAGE_SPEC=https://repo.mycompany.com/my-gpustack.whl sh -s -

# Install a specific version with extra audio dependencies.
curl -sfL https://get.gpustack.ai | INSTALL_PACKAGE_SPEC=gpustack[audio]==0.6.0 sh -s -
```

## Windows

You can use the installation script available at `https://get.gpustack.ai` to install GPUStack as a service on Windows Service Manager.

You can set additional environment variables and CLI flags when running the script. The following are examples running the installation script with different configurations:

```powershell
# Run server with the built-in worker.
Invoke-Expression (Invoke-WebRequest -Uri "https://get.gpustack.ai" -UseBasicParsing).Content

# Run server with non-default port.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --port 8080"

# Run server with a custom data path.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --data-dir 'D:\gpustack-data'"

# Run server without the built-in worker.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --disable-worker"

# Run server with TLS.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --ssl-keyfile 'C:\path\to\keyfile' --ssl-certfile 'C:\path\to\certfile'"

# Run server with external postgresql database.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --database-url 'postgresql://username:password@host:port/database_name'"

# Run worker with specified IP.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --server-url 'http://myserver' --token 'mytoken' --worker-ip '192.168.1.100'"

# Run worker with customize reserved resource.
Invoke-Expression "& { $((Invoke-WebRequest -Uri 'https://get.gpustack.ai' -UseBasicParsing).Content) } -- --server-url 'http://myserver' --token 'mytoken' --system-reserved '{""ram"":5, ""vram"":5}'"

# Install with a custom PyPI mirror.
$env:INSTALL_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple"
Invoke-Expression (Invoke-WebRequest -Uri "https://get.gpustack.ai" -UseBasicParsing).Content

# Install a custom wheel package other than releases form pypi.org.
$env:INSTALL_PACKAGE_SPEC = "https://repo.mycompany.com/my-gpustack.whl"
Invoke-Expression (Invoke-WebRequest -Uri "https://get.gpustack.ai" -UseBasicParsing).Content

# Install a specific version with extra audio dependencies.
$env:INSTALL_PACKAGE_SPEC = "gpustack[audio]==0.6.0"
Invoke-Expression (Invoke-WebRequest -Uri "https://get.gpustack.ai" -UseBasicParsing).Content
```

!!! warning

    Avoid using PowerShell ISE as it is not compatible with the installation script.

## Available Environment Variables for the Installation Script

| Name                              | Default                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `INSTALL_INDEX_URL`               | (empty)                              | Base URL of the Python Package Index.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `INSTALL_PACKAGE_SPEC`            | `gpustack[all]` or `gpustack[audio]` | The package spec to install. The install script will automatically decide based on the platform. It supports PYPI package names, URLs, and local paths. See the [pip install documentation](https://pip.pypa.io/en/stable/cli/pip_install/#pip-install) for details. <ul><li>`gpustack[all]`: With all inference backends: llama-box, vllm, vox-box.</li><li>`gpustack[vllm]`: With inference backends: llama-box, vllm.</li><li>`gpustack[audio]`: With inference backends: llama-box, vox-box.</li></ul> |
| `INSTALL_SKIP_POST_CHECK`         | (empty)                              | If set to 1, the installation script will skip the post-installation check.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `INSTALL_SKIP_BUILD_DEPENDENCIES` | `1`                                  | If set to 1 will skip the build dependencies.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `INSTALL_SKIP_IOGPU_WIRED_LIMIT`  | (empty)                              | If set to 1 will skip setting the GPU wired memory limit on macOS.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `INSTALL_IOGPU_WIRED_LIMIT_MB`    | (empty)                              | This sets the maximum amount of wired memory that the GPU can allocate on macOS.                                                                                                                                                                                                                                                                                                                                                                                                                           |

## Set Environment Variables for the GPUStack Service

You can set environment variables for the GPUStack service in an environment file located at:

- **Linux and macOS**: `/etc/default/gpustack`
- **Windows**: `$env:APPDATA\gpustack\gpustack.env`

The following is an example of the content of the file:

```bash
HF_TOKEN="your_hf_token"
HF_ENDPOINT="https://your_hf_endpoint"
```

!!!note

    Unlike Systemd, Launchd and Windows services do not natively support reading environment variables from a file. Configuration via the environment file is implemented by the installation script. It reads the file and applies the variables to the service configuration. After modifying the environment file on Windows and macOS, you need to re-run the installation script to apply changes to the GPUStack service.

## Available CLI Flags

The appended CLI flags of the installation script are passed directly as flags for the `gpustack start` command. You can refer to the [CLI Reference](../cli-reference/start.md) for details.
