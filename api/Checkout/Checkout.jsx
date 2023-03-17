import React, { useEffect } from "react";
import MercadoPago from "mercadopago";

function Checkout() {
  useEffect(() => {
    MercadoPago.configure({
      access_token: "TU_ACCESS_TOKEN",
    });
    const preference = {
      items: [
        {
          title: "Producto 1",
          unit_price: 100,
          quantity: 1,
        },
        {
          title: "Producto 2",
          unit_price: 50,
          quantity: 2,
        },
      ],
      payment_methods: {
        excluded_payment_types: [{ id: "atm" }],
        installments: 3,
      },
      back_urls: {
        success: "https://#########/checkout/success",
        failure: "https://#########/checkout/failure",
        pending: "https://#########/checkout/pending",
      },
      auto_return: "approved",
      notification_url: "https://#########/checkout/notifications",
    };
    const handler = MercadoPago.checkout({
      preference: preference,
      render: {
        container: "#button-checkout", // Selector del elemento que contiene el botón de pago
        label: "Pagar", // Texto del botón de pago
      },
    });
    handler
      .then(function (response) {
        // Manejo de la respuesta del pago exitoso
      })
      .catch(function (error) {
        // Manejo del error del pago
      });
  }, []);

  return (
    <div>
      <div id="button-checkout"></div>
    </div>
  );
}

export default Checkout;