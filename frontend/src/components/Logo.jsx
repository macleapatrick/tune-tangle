import {Flex, Box, Text, chakra} from "@chakra-ui/react";
import logo from '../assets/logo.png';  // adjust path as needed
import { col } from "framer-motion/client";


export default function Logo() {
    return (
      <Flex
        direction="column"
      >
        <Box as="img"
          src={logo}
          alt="TuneTangle Logo"
          w="1000px"
          align="center"
          mx="auto"
          boxSize="240px"         // Adjust size as needed
          mb="0"
        />
        <Text
          fontFamily="Audiowide"
          fontSize="1xl"
          color="cyan.400"
        >
        Discovering new music with
        <chakra.span color="pink.400" ml="1">Lyrical Similarity</chakra.span>
        </Text>
      </Flex>
);
}