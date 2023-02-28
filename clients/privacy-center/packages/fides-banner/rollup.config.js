import copy from "rollup-plugin-copy";
import alias from "@rollup/plugin-alias";
import esbuild from "rollup-plugin-esbuild";
import nodeResolve from "@rollup/plugin-node-resolve";
import json from "@rollup/plugin-json";

const name = require("./package.json").name;
const isDev = process.env.NODE_ENV === "development";

/**
 * @type {import('rollup').RollupOptions}
 */
export default [
  {
    input: `src/index.ts`,
    plugins: [
      // https://preactjs.com/guide/v10/getting-started/#aliasing-in-rollup
      alias({
        entries: [
          { find: "react", replacement: "preact/compat" },
          { find: "react-dom/test-utils", replacement: "preact/test-utils" },
          { find: "react-dom", replacement: "preact/compat" },
          { find: "react/jsx-runtime", replacement: "preact/jsx-runtime" },
        ],
      }),
      nodeResolve(),
      json(),
      esbuild({
        minify: !isDev,
      }),
      copy({
        // Automatically add the built script to the privacy center's static files for testing:
        targets: [{ src: `dist/${name}.js`, dest: "../../public/" }],
        verbose: true,
        hook: "writeBundle",
      }),
    ],
    output: [
      {
        // Intended for browser <script> tag - defines `Fides` global. Also supports UMD loaders.
        file: `dist/${name}.js`,
        name: "Fides",
        format: "umd",
        sourcemap: isDev,
      },
    ],
  },
];
