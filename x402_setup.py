"""Optional x402 testnet middleware. No payment is accepted without explicit configuration."""
import os
def configure_x402(app):
    if os.getenv("X402_ENABLED", "false").lower() != "true":
        return False
    address=os.getenv("X402_TESTNET_ADDRESS","")
    if not (address.startswith("0x") and len(address)==42 and all(c in "0123456789abcdefABCDEF" for c in address[2:])):
        raise RuntimeError("X402_ENABLED requires valid X402_TESTNET_ADDRESS (public wallet address only)")
    from x402.http.middleware.fastapi import PaymentMiddlewareASGI
    from x402.http import HTTPFacilitatorClient, FacilitatorConfig, PaymentOption
    from x402.http.types import RouteConfig
    from x402.server import x402ResourceServer
    from x402.mechanisms.evm.exact import ExactEvmServerScheme
    facilitator=os.getenv("X402_FACILITATOR_URL","https://x402.org/facilitator")
    server=x402ResourceServer(HTTPFacilitatorClient(FacilitatorConfig(url=facilitator)))
    server.register("eip155:84532",ExactEvmServerScheme())
    routes={"GET /premium/sample":RouteConfig(accepts=[PaymentOption(scheme="exact",price="$0.005",network="eip155:84532",pay_to=address)])}
    app.add_middleware(PaymentMiddlewareASGI,routes=routes,server=server)
    return True
