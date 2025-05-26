// src/components/VectorResults.jsx
import { Box, Text, List } from "@chakra-ui/react";

export default function VectorResults({ results, onSelect }) {
  if (!results || results.length === 0) return null;

  return (
    <Box
      mt="0"
      pt="2"
      w="full"
      maxH="200"
      mx="auto"
      overflowY="auto"
    >
      <List.Root spacing="0">
        {results.map((result) => (
          <List.Item
            key={result.id}
            px="5"
            py="3"
            display="flex"
            justifyContent="space-between"
            cursor="pointer"
            _hover={{ bg: "cyan.200" }}
            onClick={() => onSelect(result)}
          >
            <Text
              fontWeight="medium"
              fontFamily="Audiowide"
              color="gray.300"
              maxW="50%"
              isTruncated
              textAlign="left"
            >
              {result.payload?.title || "Unknown Title"}
            </Text>
            <Text
              fontSize="sm"
              fontFamily="Audiowide"
              color="gray.500"
              maxW="50%"
              isTruncated
              textAlign="right"
            >
              {result.payload?.artist || "Unknown Artist"}
            </Text>
          </List.Item>
        ))}
      </List.Root>
    </Box>
  );
}
