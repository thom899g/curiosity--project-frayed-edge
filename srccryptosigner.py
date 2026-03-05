"""
Cryptographic proof of origin system
Uses ECDSA for signing telemetry data
"""
import json
from datetime import datetime
from typing import Dict, Any
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import base64
import structlog

logger = structlog.get_logger()

class TelemetrySigner:
    """Handles cryptographic signing and verification of telemetry data"""
    
    def __init__(self, private_key_path: str = None):
        """
        Initialize signer with existing key or generate new one
        
        Args:
            private_key_path: Optional path to existing private key
        """
        self.logger = logger.bind(module="TelemetrySigner")
        
        if private_key_path:
            self._load_private_key(private_key_path)
        else:
            self._generate_key_pair()
            
        self.logger.info("signer_initialized", public_key=self.get_public_key()[:50])
    
    def _generate_key_pair(self):
        """Generate new ECDSA key pair"""
        try:
            self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
            self.public_key = self.private_key.public_key()
            self.logger.debug("key_pair_generated")
        except Exception as e:
            self.logger.error("key_generation_failed", error=str(e))
            raise
    
    def _load_private_key(self, path: str):
        """Load existing private key from file"""
        try:
            with open(path, 'rb') as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
                self.public_key = self.private_key.public_key()
            self.logger.debug("key_loaded", path=path)
        except FileNotFoundError:
            self.logger.error("key_file_not_found", path=path)
            raise
        except Exception as e:
            self.logger.error("key_load_failed", error=str(e))
            raise
    
    def get_public_key(self) -> str:
        """Get public key in PEM format"""
        try:
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo