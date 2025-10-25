# import re
# from collections import defaultdict
# from typing import Dict, List, Any
# import json
# import asyncio

# class TemplateLearner:
#     """SMART Template Learner - Gemini for both extraction AND creation"""
    
#     def __init__(self, llm_client):
#         self.llm_client = llm_client
    
#     async def analyze_contract_corpus(self, contracts: List[Dict[str, str]]) -> Dict[str, Any]:
#         """Analyze multiple contracts using Gemini for everything"""
#         print("🧠 Smart Template Learning with Gemini...")
        
#         # Step 1: Extract clauses with Gemini (SMART WAY)
#         all_clauses = await self._extract_all_clauses_with_gemini(contracts)
        
#         # Step 2: Create templates with Gemini
#         standardized_clauses = await self._create_templates_with_gemini(all_clauses)
        
#         # Step 3: Build final template
#         template = self._build_template(standardized_clauses)
        
#         print(f"✅ Learned {len(standardized_clauses)} smart templates from {len(contracts)} contracts")
#         return template
    
#     async def _extract_all_clauses_with_gemini(self, contracts: List[Dict]) -> Dict[str, List[str]]:
#         """Use Gemini to intelligently extract clauses from ALL contracts"""
#         print("🔍 Extracting clauses with Gemini...")
        
#         all_clauses_by_type = {}
#         extraction_stats = {"success": 0, "failed": 0}
        
#         for contract in contracts:
#             print(f"   🤖 Analyzing {contract['name']}...")
            
#             try:
#                 clauses = await self._extract_clauses_with_gemini(contract['text'], contract['name'])
                
#                 if clauses:
#                     extraction_stats["success"] += 1
                    
#                     # Organize clauses by type
#                     for clause_type, clause_text in clauses.items():
#                         if clause_type not in all_clauses_by_type:
#                             all_clauses_by_type[clause_type] = []
#                         all_clauses_by_type[clause_type].append(clause_text)
                        
#                     print(f"      ✅ Extracted {len(clauses)} clauses")
#                 else:
#                     extraction_stats["failed"] += 1
#                     print(f"      ⚠️  No clauses extracted")
                    
#             except Exception as e:
#                 extraction_stats["failed"] += 1
#                 print(f"      ❌ Extraction failed: {e}")
        
#         print(f"\n📊 Extraction Summary:")
#         print(f"   - Successful: {extraction_stats['success']}/{len(contracts)} contracts")
#         print(f"   - Failed: {extraction_stats['failed']}/{len(contracts)} contracts")
#         print(f"   - Clause types found: {len(all_clauses_by_type)}")
        
#         return all_clauses_by_type
    
#     async def _extract_clauses_with_gemini(self, contract_text: str, contract_name: str) -> Dict[str, str]:
#         """Gemini extraction that GUARANTEES proper JSON format"""
        
#         prompt = f"""
#         EXTRACT LEGAL CLAUSES FROM THIS CONTRACT:
        
#         {contract_text[:6000]}
        
#         **INSTRUCTIONS:**
#         1. Extract the actual clause text for each category below
#         2. Return ONLY a JSON object with these EXACT keys:
#         - "confidentiality"
#         - "limitation_of_liability"  
#         - "termination"
#         - "indemnification"
#         - "warranties"
#         - "governing_law"
#         - "intellectual_property" 
#         - "force_majeure"
#         - "payment_terms"
#         - "dispute_resolution"
        
#         3. If a clause doesn't exist, DO NOT include that key
#         4. Each value must be the EXACT clause text from the contract
#         5. Return ONLY the JSON object, no other text
        
#         **EXAMPLE OF CORRECT FORMAT:**
#         {{
#         "confidentiality": "Both parties agree to maintain confidentiality...",
#         "termination": "This agreement may be terminated with 30 days notice...",
#         "governing_law": "This agreement shall be governed by Qatar law..."
#         }}
        
#         **CRITICAL: Return ONLY valid JSON that can be parsed by json.loads()**
#         """
        
#         try:
#             response = await self.llm_client(prompt)
            
#             print(f"      📨 Raw Gemini response: {response[:300]}...")
            
#             # Clean the response
#             response = response.strip()
#             if response.startswith('```json'):
#                 response = response[7:]
#             if response.endswith('```'):
#                 response = response[:-3]
#             response = response.strip()
                
#             # Parse the JSON
#             clauses = json.loads(response)
            
#             # Validate it's the right format
#             if not isinstance(clauses, dict):
#                 print(f"      ❌ Response is not a dictionary: {type(clauses)}")
#                 return self._simple_extract_clauses(contract_text)
                
#             # Check if we got any valid clauses
#             valid_clauses = {}
#             for key, value in clauses.items():
#                 if isinstance(value, str) and len(value.strip()) > 20:  # Reasonable minimum
#                     valid_clauses[key] = value.strip()
            
#             if valid_clauses:
#                 print(f"      ✅ Gemini extracted {len(valid_clauses)} clauses: {list(valid_clauses.keys())}")
#                 return valid_clauses
#             else:
#                 print(f"      ⚠️  No valid clauses in Gemini response, using simple extraction")
#                 return self._simple_extract_clauses(contract_text)
                
#         except json.JSONDecodeError as e:
#             print(f"      ❌ JSON decode error: {e}")
#             print(f"      Response was: {response[:500]}...")
#             return self._simple_extract_clauses(contract_text)
#         except Exception as e:
#             print(f"      ❌ Gemini extraction failed: {e}")
#             return self._simple_extract_clauses(contract_text)

#     def _normalize_clause_keys(self, clauses: Dict) -> Dict[str, str]:
#         """Normalize clause keys to our standard format"""
#         if not isinstance(clauses, dict):
#             return {}
        
#         # Mapping of possible variations to our standard keys
#         key_mappings = {
#             # Confidentiality variations
#             "confidentiality": "confidentiality",
#             "Confidentiality": "confidentiality",
#             "CONFIDENTIALITY": "confidentiality",
#             "confidential": "confidentiality",
#             "Confidential": "confidentiality",
            
#             # Limitation of Liability variations
#             "limitation_of_liability": "limitation_of_liability", 
#             "Limitation_of_Liability": "limitation_of_liability",
#             "limitation of liability": "limitation_of_liability",
#             "Limitation of Liability": "limitation_of_liability",
#             "liability": "limitation_of_liability",
#             "Liability": "limitation_of_liability",
            
#             # Termination variations
#             "termination": "termination",
#             "Termination": "termination",
#             "TERMINATION": "termination",
            
#             # Governing Law variations
#             "governing_law": "governing_law",
#             "Governing_Law": "governing_law", 
#             "governing law": "governing_law",
#             "Governing Law": "governing_law",
#             "jurisdiction": "governing_law",
#             "Jurisdiction": "governing_law",
            
#             # Intellectual Property variations
#             "intellectual_property": "intellectual_property",
#             "Intellectual_Property": "intellectual_property",
#             "intellectual property": "intellectual_property", 
#             "Intellectual Property": "intellectual_property",
#             "ip": "intellectual_property",
#             "IP": "intellectual_property",
            
#             # Payment Terms variations
#             "payment_terms": "payment_terms",
#             "Payment_Terms": "payment_terms",
#             "payment terms": "payment_terms",
#             "Payment Terms": "payment_terms",
#             "payment": "payment_terms",
#             "Payment": "payment_terms",
            
#             # Force Majeure variations
#             "force_majeure": "force_majeure",
#             "Force_Majeure": "force_majeure",
#             "force majeure": "force_majeure", 
#             "Force Majeure": "force_majeure",
            
#             # Warranties variations
#             "warranties": "warranties",
#             "Warranties": "warranties",
#             "warranty": "warranties", 
#             "Warranty": "warranties",
            
#             # Indemnification variations
#             "indemnification": "indemnification",
#             "Indemnification": "indemnification",
#             "indemnity": "indemnification",
#             "Indemnity": "indemnification",
            
#             # Dispute Resolution variations
#             "dispute_resolution": "dispute_resolution",
#             "Dispute_Resolution": "dispute_resolution",
#             "dispute resolution": "dispute_resolution", 
#             "Dispute Resolution": "dispute_resolution",
#             "arbitration": "dispute_resolution",
#             "Arbitration": "dispute_resolution"
#         }
        
#         normalized = {}
#         valid_keys = [
#             "confidentiality", "limitation_of_liability", "termination", 
#             "indemnification", "warranties", "governing_law", 
#             "intellectual_property", "force_majeure", "payment_terms", "dispute_resolution"
#         ]
        
#         for key, value in clauses.items():
#             # Skip nested structures
#             if isinstance(value, (list, dict)):
#                 continue
                
#             # Normalize the key
#             normalized_key = key_mappings.get(key, key_mappings.get(key.lower(), key))
            
#             # Only include if it's one of our valid keys and the value is a string
#             if normalized_key in valid_keys and isinstance(value, str) and len(value.strip()) > 10:
#                 normalized[normalized_key] = value
        
#         return normalized
            
        
#     def _simple_extract_clauses(self, contract_text: str) -> Dict[str, str]:
#         """SIMPLE keyword-based extraction that GUARANTEES results"""
#         clauses = {}
        
#         # More comprehensive keyword patterns
#         clause_patterns = {
#             "confidentiality": [
#                 "confidential", "non-disclosure", "non disclosure", "proprietary information",
#                 "trade secrets", "confidentiality", "nonpublic", "secret", "private"
#             ],
#             "limitation_of_liability": [
#                 "limitation of liability", "liability limit", "liable", "damages", 
#                 "liability cap", "consequential damages", "indirect damages", "maximum liability"
#             ],
#             "termination": [
#                 "termination", "terminate", "expiration", "cancellation",
#                 "notice period", "termination for cause", "early termination", "end of agreement"
#             ],
#             "governing_law": [
#                 "governing law", "jurisdiction", "applicable law", "laws of",
#                 "venue", "legal framework", "qatar law", "state of", "courts of"
#             ],
#             "intellectual_property": [
#                 "intellectual property", "ip rights", "copyright", "patent",
#                 "trademark", "ownership", "work product", "inventions", "proprietary rights"
#             ],
#             "payment_terms": [
#                 "payment", "invoice", "fee", "price", "compensation",
#                 "payment terms", "due date", "net 30", "late payment", "amount payable"
#             ],
#             "force_majeure": [
#                 "force majeure", "act of god", "beyond reasonable control",
#                 "unforeseen circumstances", "natural disaster", "emergency"
#             ],
#             "warranties": [
#                 "warrant", "representation", "as is", "guarantee",
#                 "warranty", "fitness for purpose", "merchantability", "assurance"
#             ],
#             "indemnification": [
#                 "indemnif", "hold harmless", "defend", "indemnification",
#                 "indemnity", "reimbursement", "compensate"
#             ],
#             "dispute_resolution": [
#                 "dispute resolution", "arbitration", "mediation", "litigation",
#                 "disputes", "conflict resolution", "settlement"
#             ]
#         }
        
#         # Split into meaningful sections
#         sections = re.split(r'\n\s*\n|\n\s*[0-9]+\.\s+|\n\s*ARTICLE\s+[0-9]+:', contract_text)
        
#         for clause_type, keywords in clause_patterns.items():
#             best_section = None
#             best_score = 0
            
#             for section in sections:
#                 if not section or len(section.strip()) < 20:
#                     continue
                    
#                 section_lower = section.lower()
#                 # Score based on keyword matches
#                 score = sum(1 for keyword in keywords if keyword in section_lower)
                
#                 if score > best_score:
#                     best_score = score
#                     best_section = section
            
#             if best_section and best_score >= 1:
#                 clauses[clause_type] = best_section.strip()
        
#         print(f"      🔧 Simple extraction found {len(clauses)} clauses: {list(clauses.keys())}")
#         return clauses
    
#     async def _create_templates_with_gemini(self, clauses_by_type: Dict[str, List[str]]) -> Dict[str, Dict]:
#         """Use Gemini to create intelligent standard templates"""
#         standardized = {}
        
#         print(f"🔍 Creating templates from {len(clauses_by_type)} clause types...")
        
#         for clause_type, clauses in clauses_by_type.items():
#             print(f"   🤖 Creating {clause_type} template from {len(clauses)} examples...")
            
#             try:
#                 standard_version = await self._create_standard_clause_with_gemini(clauses, clause_type)
#                 common_elements = await self._analyze_common_elements_with_gemini(clauses, clause_type)
                
#                 # Ensure we have valid data
#                 if not standard_version or not isinstance(standard_version, str):
#                     standard_version = clauses[0] if clauses and isinstance(clauses[0], str) else f"Standard {clause_type} clause"
                
#                 if not common_elements or not isinstance(common_elements, list):
#                     common_elements = self._fallback_common_elements(clauses)
                
#                 standardized[clause_type] = {
#                     "standard": standard_version,
#                     "key_elements": common_elements,
#                     "sample_count": len(clauses),
#                     "confidence": min(1.0, len(clauses) / 6.0),
#                     "llm_enhanced": True,
#                     "smart_extraction": True
#                 }
#                 print(f"      ✅ Created {clause_type} template")
                
#             except Exception as e:
#                 print(f"      ❌ Template creation failed for {clause_type}: {e}")
#                 # CRITICAL: Even if Gemini fails, create a basic template
#                 standardized[clause_type] = {
#                     "standard": clauses[0] if clauses and isinstance(clauses[0], str) else f"Standard {clause_type} clause",
#                     "key_elements": self._fallback_common_elements(clauses),
#                     "sample_count": len(clauses),
#                     "confidence": 0.3,
#                     "llm_enhanced": False,
#                     "smart_extraction": True
#                 }
#                 print(f"      ⚠️  Created fallback template for {clause_type}")
        
#         print(f"✅ Template creation complete: {len(standardized)} templates created")
#         return standardized
    
#     async def _create_standard_clause_with_gemini(self, clauses: List[str], clause_type: str) -> str:
#         """Use Gemini to create optimal standard clause - IMPROVED"""
        
#         prompt = f"""
#         Create the PERFECT standard {clause_type.replace('_', ' ')} clause for QDB company.
        
#         Based on these {len(clauses)} real examples from QDB contracts:
        
#         {chr(10).join(f'--- Example {i+1} ---{chr(10)}{clause[:1000]}{chr(10)}' for i, clause in enumerate(clauses))}
        
#         Create an OPTIMAL standard clause that:
#         1. Protects QDB's interests
#         2. Is comprehensive and legally sound  
#         3. Is clear and enforceable in Qatar
#         4. Incorporates best practices from all examples
        
#         Return ONLY the clause text, no explanations or JSON.
#         """
        
#         try:
#             response = await self.llm_client(prompt)
#             return response.strip()
#         except Exception as e:
#             print(f"      ❌ Template creation failed: {e}")
#             return clauses[0] if clauses else f"Standard {clause_type} clause"
        
#     async def _analyze_common_elements_with_gemini(self, clauses: List[str], clause_type: str) -> List[str]:
#         """Use Gemini to identify key elements - SIMPLIFIED"""
        
#         prompt = f"""
#         Analyze these {len(clauses)} {clause_type} clauses from QDB contracts.
#         List the 3-5 most important legal concepts that appear in ALL of them.
        
#         Examples:
#         {chr(10).join(f'--- {i+1} ---{chr(10)}{clause[:800]}{chr(10)}' for i, clause in enumerate(clauses))}
        
#         Return ONLY a JSON array of strings like:
#         ["concept1", "concept2", "concept3"]
        
#         Keep it simple - just the key legal concepts.
#         """
        
#         try:
#             response = await self.llm_client(prompt)
#             response = response.strip()
            
#             # Clean JSON response
#             if response.startswith('```json'):
#                 response = response[7:]
#             if response.endswith('```'):
#                 response = response[:-3]
                
#             elements = json.loads(response)
            
#             # Ensure it's a list of strings
#             if isinstance(elements, list):
#                 return [str(item) for item in elements if str(item).strip()][:5]
#             else:
#                 return self._fallback_common_elements(clauses)
                
#         except Exception as e:
#             print(f"      ⚠️  Common elements failed: {e}")
#             return self._fallback_common_elements(clauses)
    
#     def _fallback_common_elements(self, clauses: List[str]) -> List[str]:
#         """Fallback method if Gemini analysis fails"""
#         all_words = []
#         for clause in clauses:
#             # Ensure clause is a string
#             if isinstance(clause, str):
#                 words = re.findall(r'\b[a-zA-Z]{4,}\b', clause.lower())
#                 all_words.extend(words)
        
#         if not all_words:
#             return ["confidential", "obligation", "protection", "duration"]
        
#         word_freq = defaultdict(int)
#         for word in all_words:
#             word_freq[word] += 1
        
#         threshold = len(clauses) * 0.6
#         common_elements = []
        
#         for word, count in word_freq.items():
#             if count >= threshold and word not in ['shall', 'party', 'agreement', 'this', 'that']:
#                 common_elements.append(word)
        
#         return common_elements[:8] if common_elements else ["key element 1", "key element 2"]
    
#     def _build_template(self, standardized_clauses: Dict) -> Dict[str, Any]:
#         """Build final template structure"""
#         template = {
#             "learned_templates": standardized_clauses,
#             "coverage_analysis": self._analyze_coverage(standardized_clauses),
#             "recommended_required_clauses": self._recommend_required_clauses(standardized_clauses),
#             "metadata": {
#                 "total_contracts_analyzed": len(standardized_clauses),
#                 "generated_at": self._get_timestamp(),
#                 "version": "3.0",
#                 "llm_enhanced": True,
#                 "smart_extraction": True
#             }
#         }
        
#         return template
    
#     def _analyze_coverage(self, clauses: Dict) -> Dict:
#         """Analyze how comprehensive the learned template is"""
#         common_clause_types = [
#             "confidentiality", "limitation_of_liability", "termination", 
#             "indemnification", "warranties", "governing_law", "intellectual_property"
#         ]
        
#         coverage = {
#             "total_clause_types": len(clauses),
#             "common_clauses_covered": sum(1 for ct in common_clause_types if ct in clauses),
#             "total_common_clauses": len(common_clause_types),
#             "coverage_percentage": (len(clauses) / len(common_clause_types)) * 100 if common_clause_types else 0,
#             "high_confidence_clauses": sum(1 for data in clauses.values() if data.get('sample_count', 0) >= 3),
#             "llm_enhanced_clauses": sum(1 for data in clauses.values() if data.get('llm_enhanced', False))
#         }
        
#         return coverage
    
#     def _recommend_required_clauses(self, clauses: Dict) -> List[str]:
#         """Recommend which clauses should be required based on frequency and confidence"""
#         required = []
#         for clause_type, data in clauses.items():
#             if data['sample_count'] >= 2 and data.get('confidence', 0) >= 0.3:
#                 required.append(clause_type)
        
#         return required
    
#     def _get_timestamp(self) -> str:
#         """Get current timestamp for metadata"""
#         from datetime import datetime
#         return datetime.now().isoformat()
import re
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime

class TemplateLearner:
    """SIMPLIFIED Template Learner - Just extract and create standards"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    async def analyze_contract_corpus(self, contracts: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze multiple contracts using Gemini"""
        print("🧠 Learning templates from QDB contracts...")
        
        # Step 1: Extract clauses with Gemini
        all_clauses = await self._extract_all_clauses_with_gemini(contracts)
        
        # Step 2: Create standard templates
        standardized_clauses = await self._create_standard_templates(all_clauses)
        
        # Step 3: Build final template
        template = self._build_template(standardized_clauses)
        
        print(f"✅ Learned {len(standardized_clauses)} standard templates from {len(contracts)} contracts")
        return template
    
    async def _extract_all_clauses_with_gemini(self, contracts: List[Dict]) -> Dict[str, List[str]]:
        """Extract clauses from ALL contracts using Gemini"""
        print("🔍 Extracting clauses with Gemini...")
        
        all_clauses_by_type = {}
        
        for contract in contracts:
            print(f"   📄 Analyzing {contract['name']}...")
            
            try:
                clauses = await self._extract_clauses_with_gemini(contract['text'])
                
                if clauses:
                    for clause_type, clause_text in clauses.items():
                        if clause_type not in all_clauses_by_type:
                            all_clauses_by_type[clause_type] = []
                        all_clauses_by_type[clause_type].append(clause_text)
                        
                    print(f"      ✅ Extracted {len(clauses)} clauses")
                else:
                    print(f"      ⚠️  No clauses extracted")
                    
            except Exception as e:
                print(f"      ❌ Extraction failed: {e}")
        
        print(f"📊 Found {len(all_clauses_by_type)} clause types across {len(contracts)} contracts")
        return all_clauses_by_type
    
    async def _extract_clauses_with_gemini(self, contract_text: str) -> Dict[str, str]:
        """Extract clauses using Gemini - SIMPLIFIED"""
        
        prompt = f"""
        EXTRACT legal clauses from this contract text.
        
        CONTRACT TEXT:
        {contract_text[:6000]}
        
        Return ONLY a JSON object with these exact keys (include only if clause exists):
        - confidentiality
        - limitation_of_liability  
        - termination
        - indemnification
        - warranties
        - governing_law
        - intellectual_property
        - force_majeure  
        - payment_terms
        - dispute_resolution

        Each value should be the EXACT clause text from the contract.
        Return ONLY valid JSON.
        """
        
        try:
            response = await self.llm_client(prompt)
            
            # Clean response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
                
            clauses = json.loads(response)
            
            # Validate and filter
            valid_clauses = {}
            for key, value in clauses.items():
                if isinstance(value, str) and len(value.strip()) > 20:
                    valid_clauses[key] = value.strip()
            
            if valid_clauses:
                print(f"      ✅ Gemini extracted {len(valid_clauses)} clauses")
                return valid_clauses
            else:
                return self._simple_extract_clauses(contract_text)
                
        except Exception as e:
            print(f"      ❌ Gemini extraction failed: {e}")
            return self._simple_extract_clauses(contract_text)

    async def _create_standard_templates(self, clauses_by_type: Dict[str, List[str]]) -> Dict[str, Dict]:
        """Create standard templates from extracted clauses"""
        standardized = {}
        
        print(f"🔧 Creating standard templates from {len(clauses_by_type)} clause types...")
        
        for clause_type, clauses in clauses_by_type.items():
            print(f"   🤖 Creating {clause_type} standard...")
            
            try:
                standard_version = await self._create_standard_clause(clauses, clause_type)
                
                standardized[clause_type] = {
                    "standard": standard_version,
                    "sample_count": len(clauses),
                    "confidence": min(1.0, len(clauses) / 5.0),  # Based on how many examples we have
                    "llm_enhanced": True
                }
                print(f"      ✅ Created standard {clause_type}")
                
            except Exception as e:
                print(f"      ❌ Failed: {e}")
                # Fallback: use first clause as standard
                standardized[clause_type] = {
                    "standard": clauses[0] if clauses else f"Standard {clause_type}",
                    "sample_count": len(clauses),
                    "confidence": 0.3,
                    "llm_enhanced": False
                }
        
        return standardized
    
    async def _create_standard_clause(self, clauses: List[str], clause_type: str) -> str:
        """Create optimal standard clause using Gemini"""
        
        prompt = f"""
        Create the BEST standard {clause_type.replace('_', ' ')} clause for QDB company.
        
        Based on these {len(clauses)} real QDB contract examples:
        
        {chr(10).join(f'--- Example {i+1} ---{chr(10)}{clause[:800]}{chr(10)}' for i, clause in enumerate(clauses))}
        
        Create a comprehensive clause that protects QDB's interests.
        Return ONLY the clause text.
        """
        
        try:
            response = await self.llm_client(prompt)
            return response.strip()
        except Exception as e:
            print(f"      ⚠️  Standard creation failed: {e}")
            return clauses[0] if clauses else f"Standard {clause_type}"
    
    def _simple_extract_clauses(self, contract_text: str) -> Dict[str, str]:
        """Fallback: simple keyword-based extraction"""
        clauses = {}
        
        # Simple keyword matching
        patterns = {
            "confidentiality": ["confidential", "non-disclosure", "proprietary"],
            "limitation_of_liability": ["limitation of liability", "liable", "damages"],
            "termination": ["termination", "terminate", "expiration"],
            "governing_law": ["governing law", "jurisdiction", "laws of"],
            "intellectual_property": ["intellectual property", "copyright", "patent"],
            "payment_terms": ["payment", "fee", "invoice", "compensation"],
            "warranties": ["warrant", "guarantee", "as is"],
            "indemnification": ["indemnif", "hold harmless", "defend"],
            "dispute_resolution": ["dispute", "arbitration", "mediation"],
            "force_majeure": ["force majeure", "act of god"]
        }
        
        sections = re.split(r'\n\s*\n', contract_text)
        
        for clause_type, keywords in patterns.items():
            for section in sections:
                if any(keyword in section.lower() for keyword in keywords):
                    clauses[clause_type] = section.strip()
                    break
        
        if clauses:
            print(f"      🔧 Simple extraction found {len(clauses)} clauses")
        return clauses
    
    def _build_template(self, standardized_clauses: Dict) -> Dict[str, Any]:
        """Build final template structure"""
        return {
            "learned_templates": standardized_clauses,
            "metadata": {
                "total_clauses_learned": len(standardized_clauses),
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        }