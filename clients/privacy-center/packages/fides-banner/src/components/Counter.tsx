import { useReducer } from "react";

export const Counter = () => {
  const [count, increment] = useReducer((prev) => prev + 1, 0);

  return (
    <div>
      <p>This is a stateful component, which shows preact acting like react.</p>
      <strong>Count: {count}</strong> <button onClick={increment}>Add 1</button>
    </div>
  );
};
