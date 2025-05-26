import { useState } from 'react'
import { Tabs, Box, Link } from "@chakra-ui/react"
import { LuMusic, LuPenLine } from "react-icons/lu"
import { Spinner, Flex } from "@chakra-ui/react";

import VectorResults from "./components/VectorResults";
import LyricSearchBar from "./components/LyricSearchBar";
import QuerySearchBar from './components/QuerySearchBar';
import Logo from "./components/Logo";
import './App.css'

export default function App() {
  const [mode, setMode] = useState('song'); // Default to song search
  const [vectorResults, setVectorResults] = useState([]);

  return (
    <main>
      <Box height="100vh" position="sticky" maxWidth="1000px" w="100%" display="flex" flexDirection="column" overflow="hidden">
        <Logo />
        <Tabs.Root defaultValue="By Song" w="100%" maxWidth="1000px" mx="auto" mt="5">
          <Tabs.List
            mb="0"
            mt="0"
          >
            <Tabs.Trigger 
              value="By Song"
              fontFamily="audiowide"
            >
              <LuMusic />
              By Song
            </Tabs.Trigger>
            <Tabs.Trigger 
              value="By Prompt"
              fontFamily="audiowide"
            >
              <LuPenLine />
              By Prompt
            </Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content 
            p="0" 
            value="By Song"
            _open={{
              animationName: "fade-in, scale-in",
              animationDuration: "300ms",
            }}
          >
            <LyricSearchBar setVectorResults={setVectorResults} />
          </Tabs.Content>
          <Tabs.Content 
            p="0" 
            value="By Prompt"
            _open={{
              animationName: "fade-in, scale-in",
              animationDuration: "300ms",
            }}
          >
            <QuerySearchBar setVectorResults={setVectorResults} />
          </Tabs.Content>
        </Tabs.Root>


        {/* Scrollable Results */}
        <Box 
            className="results-container hide-scrollbar" 
            flex="1" 
            overflowY="auto" 
            borderWidth={vectorResults.length > 0 ? "5px" : "0"} 
            borderColor={vectorResults.length > 0 ? "pink.500" : "transparent"} 
            borderRadius="md"
            p="0" 
            mt="5"
          >
            <VectorResults
              results={vectorResults}
              onSelect={(result) => {
                console.log("Selected vector result:", result);
              }}
            />
        </Box>
      </Box>
    </main>
  );
}