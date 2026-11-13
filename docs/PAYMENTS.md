# x402 testnet (Base Sepolia) — opt-in only

The free API endpoints stay free. Only `GET /premium/sample` is protected when x402 is enabled.

## Activation
1. Create a dedicated **testnet-only** EVM wallet; keep the seed phrase/private key **outside GitHub and ChatGPT**.
2. Confirm a facilitator that supports Base Sepolia (`eip155:84532`) using the [official x402 FastAPI example](https://github.com/x402-foundation/x402/tree/main/examples/python/servers/fastapi). Do not assume a production facilitator supports testnet.
3. In Render Environment set `X402_TESTNET_ADDRESS` to your **public** wallet address, `X402_FACILITATOR_URL` to the verified facilitator URL, and `X402_ENABLED=true`.
4. Redeploy. Without payment proof, `GET /premium/sample` should return HTTP 402 with the `PAYMENT-REQUIRED` header. Then use a compatible testnet client with test USDC to verify settlement.
5. To disable, set `X402_ENABLED=false` and redeploy.

**No actual testnet payment has been executed.** Testnet tokens have no monetary value. The premium endpoint is a sample and is not a monetizable product. Never enable mainnet until pricing, legal, security, and payment settlement are independently verified.

The payment integration uses the official `x402[fastapi,evm]` Python SDK. The API itself never receives wallet secrets.
