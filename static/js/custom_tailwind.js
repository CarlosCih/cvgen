tailwind.config = {
        theme: {
          extend: {
            fontFamily: { sans: ["Inter", "ui-sans-serif", "system-ui"] },
            colors: {
              brand: {
                50: "#eef2ff",
                100: "#e0e7ff",
                200: "#c7d2fe",
                300: "#a5b4fc",
                400: "#818cf8",
                500: "#6366f1",
                600: "#4f46e5",
                700: "#4338ca",
                800: "#3730a3",
                900: "#312e81",
              },
            },
            boxShadow: {
              soft: "0 10px 30px rgba(2, 6, 23, 0.08)",
              hover: "0 20px 40px rgba(2, 6, 23, 0.12)",
            },
            backgroundImage: {
              "grid-soft":
                "radial-gradient(circle at 1px 1px, rgba(99,102,241,.15) 1px, transparent 0)",
            },
          },
        },
        darkMode: "class",
      };