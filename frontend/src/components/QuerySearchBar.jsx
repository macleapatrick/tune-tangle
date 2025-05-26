// src/components/QuerySearchBar.jsx
import { useState, useEffect, useRef } from "react";
import { Box, Flex, Textarea } from "@chakra-ui/react";

function useDebounce(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

export default function QuerySearchBar({ setVectorResults }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [highlight, setHighlight] = useState(-1);
  const debounced = useDebounce(query, 300);
  const [loading, setLoading] = useState(false);


  const dropdownRef = useRef(null);

  useEffect(() => {
    if (!debounced.trim()) {
      setResults([]);
      setHighlight(-1);
      return;
    }

    fetch("/search/smart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: debounced, limit: 20 }),
    })
      .then((r) => r.json())
      .then(setResults)
      .catch(() => setResults([]));
  }, [debounced]);

  useEffect(() => {
    const close = (e) =>
      dropdownRef.current &&
      !dropdownRef.current.contains(e.target) &&
      setHighlight(-1) &&
      setResults([]);
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  function handleKey(e) {
    if (!results.length) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlight((i) => (i + 1) % results.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlight((i) => (i - 1 + results.length) % results.length);
    } else if (e.key === "Enter" && highlight >= 0) {
      select(results[highlight]);
    } else if (e.key === "Escape") {
      setResults([]);
      setHighlight(-1);
    }
  }

  function select(hit) {
    setQuery(`${hit.payload.title} – ${hit.payload.artist}`);
    setResults([]);
    setHighlight(-1);

    setLoading(true);  // <--- Start loading

    fetch("/search/vector/id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: hit.id, limit: 20 }),
    })
        .then((res) => res.json())
        .then((data) => {
        console.log("Vector API response:", data);
        setVectorResults(data);
        })
        .catch((err) => console.error("Error fetching vector data:", err))
        .finally(() => setLoading(false));  // <--- Stop loading
    }

  return (
    <Box position="relative" w="100%" mx="auto" p="0" mt="0">
      <Flex
        align="center"
        maxWidth="1000px"
        borderWidth="5px"
        borderColor="cyan.400"
        borderRadius="md"
        bg="gray.850"
        transition="all 0.2s"
      >
        <Box
          mx="4"
          boxSize="4"
          border="4px solid"
          borderColor="pink.500"
          borderRadius="full"
          position="relative"
        />
        <Textarea
          variant="subtle"
          flex="1"
          rows="4"
          fontFamily="Audiowide"
          placeholder="What do you want to hear?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKey}
          color="white"
          _placeholder={{ color: "gray.500" }}
        />
      </Flex>
    </Box>
  );
}
