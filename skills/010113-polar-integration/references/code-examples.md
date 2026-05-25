# Polar Integration — Code Examples

## 1. Sync a Product to Polar

```typescript
import { syncProductToProcessor } from "@/lib/modules/payment/polar/product-sync";

const result = await syncProductToProcessor({
  productId: "prod_xxx",
  variantId: "var_yyy", // optional
  lang: "en",
});

console.log(result.processorProductId); // "pol_zzz"
```

## 2. Create Checkout Session

```typescript
import { PolarService } from "@/lib/modules/payment/polar/service";

const lineItems = await buildLineItems(orderItems, "en");

const result = await PolarService.createCheckoutSession(
  orderId,
  orderNumber,
  lineItems,
  "USD",
  150.00,
  "en",
  "customer@example.com",
);

// Redirect user
window.location.href = result.url;
```

## 3. Confirm Payment from Webhook

```typescript
import { PaymentService } from "@/lib/modules/payment/service";

// In webhook handler
if (eventType === "order.paid") {
  const { orderId, error } = await PaymentService.confirmPayment(polarOrderId);
  if (!error) {
    // Order confirmed, orders table status set to 'confirmed'
  }
}
```

## 4. Cancel Payment

```typescript
import { cancelPaymentAction } from "@/lib/modules/payment/actions";

// User clicks "Back to Cart"
await cancelPaymentAction(orderId);
// payments record status = 'cancelled'
// orders table status reverted to 'cart'
```

## 5. Build Line Items for Checkout

```typescript
import { buildLineItems } from "@/lib/modules/payment/polar/product-sync";

const items = [
  { product_id: "p1", variant_id: null, quantity: 2, unit_price: 25.00 },
  { product_id: "p2", variant_id: "v1", quantity: 1, unit_price: 50.00 },
];

const lineItems = await buildLineItems(items, "en");
// Each item synced to Polar if needed
// Returns array with polarProductId for checkout
```

## 6. Payment Repository Queries

```typescript
import { PaymentRepository } from "@/lib/modules/payment/repository";

// Find cached processor product
const cached = await PaymentRepository.findProcessorProduct(
  db,
  productId,
  variantId,
  "USD",
  "polar",
);

// Create payment record
const payment = await PaymentRepository.createPayment(db, {
  order_id: orderId,
  amount: 150.00,
  currency_code: "USD",
  payment_url: checkoutUrl,
  redirect_url: successUrl,
});

// Update payment status from webhook
await PaymentRepository.updatePaymentStatus(db, orderId, {
  status: "paid",
  polar_order_id: "pol_order_xxx",
  paid_at: new Date().toISOString(),
});
```

## 7. Raw Polar API Calls

```typescript
import {
  polarCreateProduct,
  polarGetProduct,
  polarUpdateProduct,
  polarCreateCheckout,
} from "@/lib/modules/payment/polar/client";

// Create product
const product = await polarCreateProduct({
  name: "My Product",
  description: "Product description",
  prices: [{
    amount_type: "fixed",
    price_amount: 2500, // cents
    price_currency: "usd",
  }],
  metadata: { product_id: "prod_xxx" },
});

// Create checkout
const checkout = await polarCreateCheckout({
  products: [product.id],
  success_url: "https://example.com/success",
  cancel_url: "https://example.com/cancel",
  customer_email: "user@example.com",
  metadata: { order_id: "ord_xxx" },
});
```
